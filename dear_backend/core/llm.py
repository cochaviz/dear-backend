import logging
import sys

from bs4 import BeautifulSoup as Soup
from dear_backend.config import (
    INDEX_PERSIST_DIRECTORY,
    INIT_INDEX,
    TARGET_URL,
)
from dear_backend.core.models.question import Question
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.utils.html import PREFIXES_TO_IGNORE_REGEX, SUFFIXES_TO_IGNORE_REGEX
from langchain.vectorstores import Chroma
from langchain_community.llms import Ollama

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


global conversation
conversation = None


def init_index():
    if not INIT_INDEX:
        logging.info("continue without initializing index")
        return

    # scrape data from web
    documents = RecursiveUrlLoader(
        TARGET_URL,
        max_depth=4,
        extractor=lambda x: Soup(x, "html.parser").text,
        prevent_outside=True,
        use_async=True,
        timeout=600,
        check_response_status=True,
        # drop trailing / to avoid duplicate pages.
        link_regex=(
            f"href=[\"']{PREFIXES_TO_IGNORE_REGEX}((?:{SUFFIXES_TO_IGNORE_REGEX}.)*?)"
            r"(?:[\#'\"]|\/[\#'\"])"
        ),
    ).load()

    logging.info("index creating with `%d` documents", len(documents))

    # split text
    # this chunk_size and chunk_overlap effects to the prompt size
    # execeed promt size causes error `prompt size exceeds the context window size and cannot be processed`
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(documents)

    # create embeddings with huggingface embedding model `all-MiniLM-L6-v2`
    # then persist the vector index on vector db
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=INDEX_PERSIST_DIRECTORY,
    )
    vectordb.persist()


def init_conversation():
    global conversation

    # load index
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(
        persist_directory=INDEX_PERSIST_DIRECTORY, embedding_function=embeddings
    )

    # llama2 llm which runs with ollama
    # ollama expose an api for the llam in `localhost:11434`
    llm = Ollama(
        model="llama2",
        base_url="http://localhost:11434",
        verbose=True,
    )

    # create conversation
    conversation = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        verbose=True,
    )


def chat(question: Question):
    global conversation
    assert conversation is not None, "conversation is not initialized"

    chat_history = []
    response = conversation(
        {"question": question.content, "chat_history": chat_history}
    )
    answer = response["answer"]

    logging.info("got response from llm - %s", answer)

    # TODO save history

    return answer

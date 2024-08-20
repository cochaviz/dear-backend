from logging import Logger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from dear_backend.core.llm import chat
from dear_backend.core.models.question import Question

logger = Logger(__name__)

app = FastAPI()
CORSMiddleware(
    app,
    allow_origins=["localhost", "appa.cochaviz.internal", "diary.cochaviz.internal"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """
    Redirect to api status
    """
    return RedirectResponse(url="/api/status")


@app.get("/api/status")
def status():
    """
    Return status of the database and LLM. This includes
    the last time the database was synced.
    """
    return {"message": "We're up!"}


@app.post("/api/question")
def post_question(question: Question):
    """
    Return a question from the database.
    """

    logger.info(question)
    resp = chat(question)

    return {"answer": resp}

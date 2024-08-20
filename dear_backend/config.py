import os

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

ALLOWED_ORIGINS: list[str] = [
    "http://diary.cochaviz.internal",
    "https://diary.cochaviz.ineternal",
    "http://localhost",
] + os.getenv("ALLOWED_ORIGINS", "").split(",")

# environment variables

INIT_INDEX = os.getenv("INIT_INDEX") is not None
INDEX_PERSIST_DIRECTORY = os.getenv("DATA_DIR", "./data/chromadb")

TARGET_URL = "http://diary.cochaviz.internal/entries/all"
BACKEND_PORT = os.getenv("API_PORT", 8081)

DEV_MODE: bool = os.getenv("DEV_MODE") is not None

# NOTE: For now, conversations will be ephemeral
# # mongodb config host, username, password
# MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
# MONGO_PORT = os.getenv("MONGO_PORT", 27017)
# MONGO_USER = os.getenv("MONGO_USER", "testuser")
# MONGO_PASS = os.getenv("MONGO_PASS", "testpass")

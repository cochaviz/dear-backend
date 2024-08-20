import uvicorn

from dear_backend.config import BACKEND_PORT, DEV_MODE

if __name__ == "__main__":
    uvicorn.run(
        "dear_backend.main:app",
        host="localhost",
        reload=DEV_MODE,
        port=BACKEND_PORT,  # type: ignore
    )

import uvicorn
from fastapi import FastAPI
from app.routers import firestore, pubsub, storage
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import logging

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="GCP FastAPI Example with Google Auth")

# Configure CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://appointmentstoday-web-services.vercel.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router modules
app.include_router(firestore.router, prefix="/firestore", tags=["Firestore"])
app.include_router(pubsub.router, prefix="/pubsub", tags=["PubSub"])
app.include_router(storage.router, prefix="/storage", tags=["Storage"])

@app.get("/health", tags=["Health"])
def health_check():
    logger.info("Health check requested")
    return {"status": "OK"}

if __name__ == "__main__":
    # For local testing: python -m app.main
    logger.info("Starting Uvicorn server")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

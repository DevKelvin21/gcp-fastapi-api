import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from google.cloud import firestore, storage, pubsub_v1
from pydantic import BaseModel

app = FastAPI(title="GCP-FastAPI-API")

firestore_client = firestore.Client()
storage_client = storage.Client()
pubsub_client = pubsub_v1.PublisherClient()

ENV_VAR_MSG = "Specified environment variable is not set."

FIRESTORE_COLLECTION = os.environ.get("FIRESTORE_COLLECTION", ENV_VAR_MSG)
BUCKET_NAME = os.environ.get("BUCKET_NAME", ENV_VAR_MSG)
PUBSUB_TOPIC = os.environ.get("PUBSUB_TOPIC", ENV_VAR_MSG)

# A simple Pydantic model for demonstration
class Item(BaseModel):
    name: str
    description: str

@app.get("/health")
def health_check():
    return {"status": "OK"}

# 1) Firestore: Create a document
@app.post("/firestore/create")
def create_firestore_doc(item: Item):
    doc_ref = firestore_client.collection(FIRESTORE_COLLECTION).document()
    doc_ref.set(item.dict())
    return {"message": "Document created", "doc_id": doc_ref.id}

# 2) Firestore: Read a document by doc_id
@app.get("/firestore/{doc_id}")
def read_firestore_doc(doc_id: str):
    doc_ref = firestore_client.collection(FIRESTORE_COLLECTION).document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Document not found")

# 3) GCS: Upload a file
@app.post("/storage/upload")
async def upload_file_to_gcs(file: UploadFile = File(...)):
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file.filename)
        # .read() loads the entire file into memory; for large files consider streaming
        blob.upload_from_string(await file.read(), content_type=file.content_type)
        return {"message": "File uploaded", "file_name": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4) GCS: Download a file
@app.get("/storage/download/{filename}")
def download_file_from_gcs(filename: str):
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    if not blob.exists():
        raise HTTPException(status_code=404, detail="File not found in bucket")
    data = blob.download_as_bytes()
    # Return as a base64 string, or direct bytes, or even a file response
    return {"filename": filename, "content_size": len(data)}

# 5) Pub/Sub: Publish a message
@app.post("/pubsub/publish")
def publish_message(message: str):
    # message param can be anything, e.g. JSON string
    if PUBSUB_TOPIC.startswith("projects/") is False:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid PUBSUB_TOPIC format: {PUBSUB_TOPIC}"
        )
    data = message.encode("utf-8")
    future = pubsub_client.publish(PUBSUB_TOPIC, data=data)
    message_id = future.result()
    return {"message_id": message_id, "message": message}


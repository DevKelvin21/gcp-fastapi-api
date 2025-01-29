import os
from google.cloud import storage
from fastapi import UploadFile

ENV_VAR_MSG = "Specified environment variable is not set."

class StorageService:
    def __init__(self):
        self.client = storage.Client()
        self.bucket_name = os.environ.get("BUCKET_NAME", ENV_VAR_MSG)

    async def upload_file(self, file: UploadFile) -> str:
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(file.filename)
        blob.upload_from_string(await file.read(), content_type=file.content_type)
        return file.filename

    def download_file(self, filename: str) -> bytes:
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(filename)
        if not blob.exists():
            return None
        return blob.download_as_bytes()

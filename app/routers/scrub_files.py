from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks, Query
from fastapi.responses import JSONResponse, StreamingResponse
from datetime import datetime
import json
import io
import os
import asyncio
import mimetypes

from app.services.firestore_service import FirestoreService
from app.services.storage_service import StorageService
from app.services.pubsub_service import PubSubService
from app.models.item import Item, Status, OutputFiles
from app.models.file_type import FileType
from app.models.pubsub_message import PubSubMessage
from app.utils import make_serializable
from app.auth_google import google_auth_dependency #TODO: implement auth for scrub-files

router = APIRouter(
    prefix="/scrub-files",
    tags=["Scrub Files"],
)
    #FIXME: dependencies=[Depends(google_auth_dependency)],

firestore_service = FirestoreService()
storage_service = StorageService()
pubsub_service = PubSubService()

@router.get("/list")
async def list_files():
    """
    List all uploaded files and their statuses.
    """
    try:
        documents = firestore_service.list_documents()
        files_serializable = []
        for doc in documents:
            doc_serializable = make_serializable(doc)
            files_serializable.append(doc_serializable)

        return JSONResponse(
            status_code=200,
            content={"data": files_serializable},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    fileConfig: str = Form(...),
):
    """
    Upload a file to Google Cloud Storage and save its configuration to Firestore.
    """
    try:
        file_config_data = json.loads(fileConfig)
        file_config = Item(**file_config_data)

        storage_path = f"uploads/{file_config.file_name}"
        await storage_service.upload_file(file, storage_path)

        file_config.status = Status(stage="UPLOADED", last_updated=datetime.utcnow())
        file_config.output_files = OutputFiles(
            base_file_path=storage_path,
            clean_file_path=file_config.output_files.clean_file_path or "",
            invalid_file_path=file_config.output_files.invalid_file_path or "",
            dnc_file_path=file_config.output_files.dnc_file_path or ""
        )

        doc_id = firestore_service.create_document(file_config.dict(by_alias=True))

        message = PubSubMessage(
            fileId=doc_id,
            bucket=os.getenv("BUCKET_NAME"),
            fileName=file_config.file_name,
            configDocumentPath=f"{os.getenv('FIRESTORE_COLLECTION')}/{doc_id}",
        )
        background_tasks.add_task(pubsub_service.publish_message, message.dict())

        return JSONResponse(
            status_code=200,
            content={"message": "File uploaded and config saved.", "id": doc_id},
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON for fileConfig.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{id}")
async def get_status(id: str):
    """
    Retrieve the processing status of the file.
    """
    try:
        file_config = firestore_service.get_document(id)
        if not file_config:
            raise HTTPException(status_code=404, detail="FileConfig not found.")

        return JSONResponse(
            status_code=200,
            content=file_config.status.dict(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define the mapping
FILE_TYPE_MAPPING = {
    FileType.clean: "cleanFilePath",
    FileType.invalid: "invaldFilePath",
    FileType.dnc: "dncFilePath",
}

@router.get("/download/{id}")
async def download_results(
    id: str,
    file_type: FileType = Query(..., description="Type of file to download: clean, invalid, dnc")
):
    """
    Download a specific processing results file if processing is completed.
    """
    try:
        file_config = firestore_service.get_document(id)
        if not file_config:
            raise HTTPException(status_code=404, detail="FileConfig not found.")

        if file_config.get('status', {}).get('stage') != "DONE":
            raise HTTPException(
                status_code=400, detail="Processing not completed yet."
            )

        output_files = file_config.get('outputFiles', {})
        storage_key = FILE_TYPE_MAPPING.get(file_type)

        if not storage_key:
            raise HTTPException(status_code=400, detail=f"Invalid file_type '{file_type.value}'.")

        storage_path = output_files.get(storage_key)

        if not storage_path:
            raise HTTPException(status_code=404, detail=f"File type '{file_type}' not found.")

        file_bytes = await asyncio.to_thread(storage_service.download_file, storage_path)

        if not file_bytes:
            raise HTTPException(status_code=404, detail="File not found in storage.")

        filename = os.path.basename(storage_path)
        file_like = io.BytesIO(file_bytes)
        media_type, _ = mimetypes.guess_type(filename)
        if not media_type:
            media_type = 'application/octet-stream'  # Fallback

        return StreamingResponse(
            file_like,
            media_type=media_type,
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

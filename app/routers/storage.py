from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.auth_google import google_auth_dependency
from app.services.storage_service import StorageService
from app.models.claims import GoogleClaims

router = APIRouter()
storage_service = StorageService()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), claims: GoogleClaims = Depends(google_auth_dependency)):
    """
    Uploads a file to GCS. Protected by Google ID token.
    """
    try:
        file_name = await storage_service.upload_file(file)
        return {"message": "File uploaded", "file_name": file_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{filename}")
def download_file(filename: str, claims: GoogleClaims = Depends(google_auth_dependency)):
    """
    Downloads a file from GCS. Protected by Google ID token.
    """
    try:
        file_content = storage_service.download_file(filename)
        if file_content is None:
            raise HTTPException(status_code=404, detail="File not found")
        # For demonstration, returning a preview. Adjust as needed.
        return {
            "filename": filename,
            "size": len(file_content),
            "content_preview": file_content[:100].decode("utf-8", errors="replace")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
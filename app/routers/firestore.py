from fastapi import APIRouter, Depends, HTTPException, status
from app.auth_google import google_auth_dependency
from app.models.item import Item
from app.services.firestore_service import FirestoreService
from app.models.claims import GoogleClaims

router = APIRouter()
firestore_service = FirestoreService()

@router.post("/create")
def create_document(item: Item, claims: GoogleClaims = Depends(google_auth_dependency)):
    """
    Create a Firestore document with the given item data.
    Requires a valid Google ID token from the front-end.
    """
    doc_id = firestore_service.create_document(item.dict())
    return {"message": "Document created", "doc_id": doc_id}

@router.get("/{doc_id}")
def get_document(doc_id: str, claims: GoogleClaims = Depends(google_auth_dependency)):
    doc = firestore_service.get_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return doc

@router.put("/{doc_id}")
def update_document(doc_id: str, item: Item, claims: GoogleClaims = Depends(google_auth_dependency)):
    updated = firestore_service.update_document(doc_id, item.dict())
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return {"message": "Document updated"}

@router.delete("/{doc_id}")
def delete_document(doc_id: str, claims: GoogleClaims = Depends(google_auth_dependency)):
    deleted = firestore_service.delete_document(doc_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return {"message": "Document deleted"}

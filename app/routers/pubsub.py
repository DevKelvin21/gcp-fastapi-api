from fastapi import APIRouter, Depends, HTTPException
from app.auth_google import google_auth_dependency
from app.services.pubsub_service import PubSubService
from app.models.claims import GoogleClaims

router = APIRouter()
pubsub_service = PubSubService()

@router.post("/publish")
def publish_message(message: str, claims: GoogleClaims = Depends(google_auth_dependency)):
    """
    Publishes a message to Pub/Sub. Requires valid Google ID token.
    """
    try:
        message_id = pubsub_service.publish_message(message)
        return {"message_id": message_id, "message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

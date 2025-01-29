import os
import time
import google.auth.transport.requests
import google.oauth2.id_token
from google.cloud import firestore
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models.claims import GoogleClaims

# OAuth2 scheme to extract Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="dummy")

_client_id_cache = {
    "last_update": 0.0,
    "cache_ttl": 60.0,
    "client_ids": set()
}

def get_valid_client_ids_from_firestore() -> set:
    now = time.time()
    if now - _client_id_cache["last_update"] < _client_id_cache["cache_ttl"]:
        # Return cached version
        return _client_id_cache["client_ids"]
    # Otherwise fetch from Firestore
    db = firestore.Client()
    new_ids = set()
    docs = db.collection("allowedClientIDs").stream()
    for doc in docs:
        data = doc.to_dict()
        cid = data.get("clientId")
        if cid:
            new_ids.add(cid)
    # Update cache
    _client_id_cache["client_ids"] = new_ids
    _client_id_cache["last_update"] = now
    return new_ids

def verify_google_id_token(id_token: str) -> GoogleClaims:
    """
    Verifies the Google ID token and checks if its audience is allowed.
    Returns a GoogleClaims instance if valid.
    """
    try:
        request = google.auth.transport.requests.Request()
        # Verify the token without specifying 'audience'
        decoded_claims = google.oauth2.id_token.verify_oauth2_token(
            id_token, request, audience=None
        )
    except ValueError as e:
        # Invalid token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google ID token: {str(e)}"
        )

    # Ensure the token is issued by Google
    if decoded_claims.get("iss") not in {"accounts.google.com", "https://accounts.google.com"}:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid issuer."
        )

    # Check if the 'aud' (audience) is in the allowed list
    aud = decoded_claims.get("aud")
    if not aud:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ID token missing 'aud' claim."
        )

    allowed_client_ids = get_valid_client_ids_from_firestore()
    if aud not in allowed_client_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Token audience '{aud}' is not allowed."
        )

    # Return the claims as a GoogleClaims instance
    return GoogleClaims(**decoded_claims)

def google_auth_dependency(token: str = Depends(oauth2_scheme)) -> GoogleClaims:
    """
    FastAPI dependency to verify Google ID tokens.
    Returns a GoogleClaims instance if valid.
    """
    return verify_google_id_token(token)
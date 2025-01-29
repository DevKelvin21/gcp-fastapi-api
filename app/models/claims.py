from pydantic import BaseModel, EmailStr
from typing import Optional

class GoogleClaims(BaseModel):
    iss: str
    azp: Optional[str] = None
    aud: str
    sub: str
    email: Optional[EmailStr] = None
    email_verified: Optional[bool] = None
    at_hash: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    locale: Optional[str] = None
    # Add other fields as needed based on your application's requirements

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PubSubMessage(BaseModel):
    fileId: str
    bucket: str
    fileName: str
    configDocumentPath: str
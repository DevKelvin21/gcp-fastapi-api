from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class Status(BaseModel):
    stage: str
    last_updated: datetime

class OutputFiles(BaseModel):
    clean_file_path: Optional[str] = None
    invalid_file_path: Optional[str] = None
    dnc_file_path: Optional[str] = None

class Item(BaseModel):
    file_name: str
    uploaded_by_user_id: str
    phone_columns: List[str]
    column_aliases: Dict[str, str]
    phone_column_indexes: List[int]
    phone_order_indexes: List[int]
    has_header_row: bool
    timestamp: datetime
    status: Status  # Direct reference
    output_files: Optional[OutputFiles] = None  # Direct reference

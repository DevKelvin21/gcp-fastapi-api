from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

def to_camel(string: str) -> str:
    """Convert snake_case to camelCase."""
    parts = string.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

class CamelModel(BaseModel):
    """Base model with camelCase alias generator."""
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        allow_population_by_alias = True

class Status(CamelModel):
    stage: str
    last_updated: datetime

class OutputFiles(CamelModel):
    base_file_path: Optional[str] = Field(None, alias="baseFilePath")
    clean_file_path: Optional[str] = Field(None, alias="cleanFilePath")
    invalid_file_path: Optional[str] = Field(None, alias="invalidFilePath")
    dnc_file_path: Optional[str] = Field(None, alias="dncFilePath")

class Item(CamelModel):
    file_name: str = Field(..., alias="fileName")
    uploaded_by_user_id: str = Field(..., alias="uploadedByUserId")
    phone_columns: List[str] = Field(..., alias="phoneColumns")
    column_aliases: Dict[str, str] = Field(..., alias="columnAliases")
    phone_column_indexes: List[int] = Field(..., alias="phoneColumnIndexes")
    phone_order_indexes: List[int] = Field(..., alias="phoneOrderIndexes")
    has_header_row: bool = Field(..., alias="hasHeaderRow")
    timestamp: datetime
    status: Status
    output_files: OutputFiles = Field(..., alias="outputFiles")

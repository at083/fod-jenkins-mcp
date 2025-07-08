from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ErrorModel(BaseModel):
    code: str
    message: str

class GetJobInfoOutput(BaseModel):
    job: Optional[Dict[str, Any]] = None
    summary: str
    error: Optional[ErrorModel] = None

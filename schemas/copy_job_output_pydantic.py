from pydantic import BaseModel
from typing import Optional, Dict

class CopyJobOutput(BaseModel):
    success: bool
    summary: str
    error: Optional[Dict] = None

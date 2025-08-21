from pydantic import BaseModel
from typing import Optional, Dict

class FoDSubmitJobOutput(BaseModel):
    success: bool
    output: Optional[str] = None
    summary: str
    error: Optional[Dict] = None

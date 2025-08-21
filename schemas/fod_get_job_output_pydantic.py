from pydantic import BaseModel
from typing import Optional, Dict, Any

class FoDGetJobOutput(BaseModel):
    job: Optional[Dict[str, Any]] = None
    summary: str
    error: Optional[Dict] = None

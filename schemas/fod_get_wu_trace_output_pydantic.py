from pydantic import BaseModel
from typing import Optional, Dict, Any

class FoDGetWuTraceOutput(BaseModel):
    trace: Optional[Any] = None
    summary: str
    error: Optional[Dict] = None

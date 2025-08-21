from pydantic import BaseModel
from typing import Optional, Any, Dict

class FoDGetHbmMemoryDumpsOutput(BaseModel):
    outputs: Optional[Any] = None
    summary: str
    error: Optional[Dict] = None

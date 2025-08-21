from pydantic import BaseModel
from typing import Optional, Any, Dict

class FoDGetCoreDumpOutputsOutput(BaseModel):
    outputs: Optional[Any] = None
    summary: str
    error: Optional[Dict] = None

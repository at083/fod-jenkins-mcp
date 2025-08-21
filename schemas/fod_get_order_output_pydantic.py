from pydantic import BaseModel
from typing import Optional, Any, Dict

class FoDGetOrderOutput(BaseModel):
    order: Optional[Any] = None
    summary: str
    error: Optional[Dict] = None

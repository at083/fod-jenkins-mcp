from pydantic import BaseModel
from typing import Optional, Any, Dict

class FoDGetFunctionTraceOutput(BaseModel):
    trace: Optional[Any] = None
    summary: str
    error: Optional[Dict] = None

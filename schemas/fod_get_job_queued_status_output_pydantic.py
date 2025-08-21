from pydantic import BaseModel
from typing import Optional, Dict, Any

class FoDGetJobQueuedStatusOutput(BaseModel):
    queue_status: Optional[Dict[str, Any]] = None
    summary: str
    error: Optional[Dict] = None

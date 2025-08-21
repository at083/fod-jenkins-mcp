from pydantic import BaseModel
from typing import Optional, Dict, Any

class FoDGetClusterStatusOutput(BaseModel):
    status: Optional[Dict[str, Any]] = None
    summary: str
    error: Optional[Dict] = None

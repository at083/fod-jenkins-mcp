from pydantic import BaseModel
from typing import Optional, Dict, Any

class FoDGetRobotStateOutput(BaseModel):
    robotstate: Optional[Dict[str, Any]] = None
    summary: str
    error: Optional[Dict] = None

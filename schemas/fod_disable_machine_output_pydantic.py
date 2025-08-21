from pydantic import BaseModel
from typing import Optional, Dict

class FoDDisableMachineOutput(BaseModel):
    summary: str
    error: Optional[Dict] = None

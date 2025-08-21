from pydantic import BaseModel
from typing import Optional, Dict

class FoDEnableMachineOutput(BaseModel):
    summary: str
    error: Optional[Dict] = None

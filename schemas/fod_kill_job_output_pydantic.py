from pydantic import BaseModel
from typing import Optional, Dict

class FoDKillJobOutput(BaseModel):
    summary: str
    error: Optional[Dict] = None

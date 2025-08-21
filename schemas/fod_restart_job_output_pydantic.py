from pydantic import BaseModel
from typing import Optional, Dict

class FoDRestartJobOutput(BaseModel):
    summary: str
    error: Optional[Dict] = None

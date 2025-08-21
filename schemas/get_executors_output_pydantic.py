from pydantic import BaseModel
from typing import Optional, Dict

class GetExecutorsOutput(BaseModel):
    executors: Optional[Dict] = None
    summary: str
    error: Optional[Dict] = None

from pydantic import BaseModel
from typing import Optional, Dict

class FoDEnableClusterOutput(BaseModel):
    summary: str
    error: Optional[Dict] = None

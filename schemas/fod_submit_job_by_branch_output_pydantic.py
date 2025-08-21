from pydantic import BaseModel
from typing import Optional, Dict

class FoDSubmitJobByBranchOutput(BaseModel):
    status: int
    location: Optional[str] = None
    response: Optional[str] = None
    summary: str
    error: Optional[Dict] = None

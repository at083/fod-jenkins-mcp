from pydantic import BaseModel
from typing import Optional, Dict

class FoDGetHumanFileOutput(BaseModel):
    content: Optional[str] = None
    summary: str
    error: Optional[Dict] = None

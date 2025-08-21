from pydantic import BaseModel
from typing import Optional

class FoDGetNightlyHistoryInput(BaseModel):
    days: Optional[int] = None
    tags: Optional[str] = None
    owner: Optional[str] = None
    state: Optional[str] = None
    sort: Optional[str] = None
    session_id: Optional[str] = None

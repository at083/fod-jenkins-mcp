from pydantic import BaseModel
from typing import Optional
class FoDArchiveJobInput(BaseModel):
    job_id: str
    archive: bool  # True to archive, False to unarchive
    days: Optional[int] = None
    session_id: str = None

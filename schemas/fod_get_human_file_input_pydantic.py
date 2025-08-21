from pydantic import BaseModel
from typing import Optional
class FoDGetHumanFileInput(BaseModel):
    job_id: str
    file_name: str
    filter_level: Optional[str] = None
    session_id: str = None

from pydantic import BaseModel
from typing import Optional
class FoDUpdateJobPriorityInput(BaseModel):
    job_id: str
    priority: int  # 0 (low), 1 (medium), 2 (high), 3 (critical)
    session_id: str = None

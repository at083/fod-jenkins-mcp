from pydantic import BaseModel
from typing import Optional, Dict
class FoDUpdateJobMetadataInput(BaseModel):
    job_id: str
    metadata: Dict[str, Optional[str]]
    session_id: str = None

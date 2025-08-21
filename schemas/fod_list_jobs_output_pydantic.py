from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class FoDListJobsOutput(BaseModel):
    jobs: Optional[List[Dict[str, Any]]] = None
    jobs_count: Optional[int] = None
    summary: str
    error: Optional[Dict] = None

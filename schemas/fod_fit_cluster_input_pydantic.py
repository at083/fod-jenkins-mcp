from pydantic import BaseModel
from typing import Optional
class FoDFitClusterInput(BaseModel):
    cluster_id: str
    job_requirements: Optional[dict] = None
    session_id: str = None

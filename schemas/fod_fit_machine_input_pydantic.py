from pydantic import BaseModel
from typing import Optional
class FoDFitMachineInput(BaseModel):
    machine_id: str
    job_requirements: Optional[dict] = None
    session_id: str = None

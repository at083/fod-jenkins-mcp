from pydantic import BaseModel
from typing import Optional
class FoDGetTelemetryInput(BaseModel):
    job_id: str
    vars: Optional[str] = None  # Comma-separated list of telemetry variables
    session_id: str = None

from pydantic import BaseModel
from typing import Optional, Any, Dict

class FoDGetTelemetryOutput(BaseModel):
    telemetry: Optional[Any] = None
    summary: str
    error: Optional[Dict] = None

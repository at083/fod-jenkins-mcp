from pydantic import BaseModel
from typing import Optional, Dict, Any

class FoDFitMachineOutput(BaseModel):
    fit_result: Optional[Dict[str, Any]] = None
    summary: str
    error: Optional[Dict] = None

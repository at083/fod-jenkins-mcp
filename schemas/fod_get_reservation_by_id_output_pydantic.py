from pydantic import BaseModel
from typing import Optional, Dict, Any

class FoDGetReservationByIdOutput(BaseModel):
    reservation: Optional[Dict[str, Any]] = None
    summary: str
    error: Optional[Dict] = None

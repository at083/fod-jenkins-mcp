from pydantic import BaseModel
from typing import Optional, Dict

class FoDCancelReservationOutput(BaseModel):
    summary: str
    error: Optional[Dict] = None

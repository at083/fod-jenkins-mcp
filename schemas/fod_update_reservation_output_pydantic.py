from pydantic import BaseModel
from typing import Optional, Dict

class FoDUpdateReservationOutput(BaseModel):
    summary: str
    error: Optional[Dict] = None

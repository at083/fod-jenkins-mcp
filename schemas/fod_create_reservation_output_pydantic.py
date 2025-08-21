from pydantic import BaseModel
from typing import Optional, Dict

class FoDCreateReservationOutput(BaseModel):
    summary: str
    error: Optional[Dict] = None

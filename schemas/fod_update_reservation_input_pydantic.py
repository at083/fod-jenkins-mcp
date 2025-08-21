from pydantic import BaseModel
from typing import Optional
class FoDUpdateReservationInput(BaseModel):
    reservation_id: str
    owner: str
    resource: str
    start_time: str  # ISO8601
    end_time: str    # ISO8601
    session_id: str = None

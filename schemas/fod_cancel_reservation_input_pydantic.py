from pydantic import BaseModel
class FoDCancelReservationInput(BaseModel):
    reservation_id: str
    session_id: str = None

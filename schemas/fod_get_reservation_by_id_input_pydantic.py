from pydantic import BaseModel
class FoDGetReservationByIdInput(BaseModel):
    reservation_id: str
    session_id: str = None

from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class FoDGetReservationsOutput(BaseModel):
    reservations: Optional[List[Dict[str, Any]]] = None
    summary: str
    error: Optional[Dict] = None

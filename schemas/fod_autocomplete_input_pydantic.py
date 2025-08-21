from pydantic import BaseModel
from typing import Optional
class FoDAutocompleteInput(BaseModel):
    field_name: str
    q: Optional[str] = None
    limit: Optional[int] = 10
    session_id: str = None

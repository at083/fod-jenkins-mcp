from pydantic import BaseModel
from typing import Optional

class FoDListJobsInput(BaseModel):
    owner: Optional[str] = None
    tags: Optional[str] = None
    state: Optional[str] = None
    hardware_model: Optional[str] = None
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort: Optional[str] = None
    session_id: Optional[str] = None
    # Add more filters as needed

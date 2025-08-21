from pydantic import BaseModel
from typing import List, Optional

class FoDSubmitJobInput(BaseModel):
    funos_binary: str
    blobs: Optional[List[str]] = None
    hardware_model: Optional[str] = None
    duration: Optional[int] = None
    tags: Optional[str] = None
    note: Optional[str] = None
    params_file: Optional[str] = None
    extra_args: Optional[List[str]] = None
    session_id: Optional[str] = None

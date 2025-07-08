from pydantic import BaseModel
from typing import Optional

class GetBuildConsoleOutputInput(BaseModel):
    job_name: str
    build_number: int
    start_line: int = 0
    num_lines: int = 500
    search: Optional[str] = None
    session_id: Optional[str] = None

from pydantic import BaseModel
from typing import Optional

class GetBuildConsoleOutputOutput(BaseModel):
    job_name: str
    build_number: int
    console: str
    total_lines: int
    start_line: int
    end_line: int
    has_more: bool
    search: Optional[str]
    summary: str
    error: Optional[dict] = None

from pydantic import BaseModel
class FoDGetWuTraceInput(BaseModel):
    job_id: str
    session_id: str = None

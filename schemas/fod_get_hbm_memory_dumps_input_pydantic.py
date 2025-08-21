from pydantic import BaseModel
class FoDGetHbmMemoryDumpsInput(BaseModel):
    job_id: str
    session_id: str = None

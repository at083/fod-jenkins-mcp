from pydantic import BaseModel
class FoDGetJobInput(BaseModel):
    job_id: str
    session_id: str = None

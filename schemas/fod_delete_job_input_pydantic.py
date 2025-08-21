from pydantic import BaseModel
class FoDDeleteJobInput(BaseModel):
    job_id: str
    session_id: str = None

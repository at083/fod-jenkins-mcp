from pydantic import BaseModel
class FoDKillJobInput(BaseModel):
    job_id: str
    session_id: str = None

from pydantic import BaseModel
class FoDRestartJobInput(BaseModel):
    job_id: str
    session_id: str = None

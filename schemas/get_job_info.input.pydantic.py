from pydantic import BaseModel, Field

class GetJobInfoInput(BaseModel):
    job_name: str = Field(..., description="Jenkins job name")
    session_id: str = None

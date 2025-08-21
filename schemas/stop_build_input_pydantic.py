from pydantic import BaseModel, Field

class StopBuildInput(BaseModel):
    job_name: str = Field(..., description="Jenkins job name")
    build_number: int = Field(..., description="Jenkins build number to stop")
    session_id: str = None

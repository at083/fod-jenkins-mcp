from pydantic import BaseModel, Field

class StopBuildOutput(BaseModel):
    success: bool = Field(..., description="True if the build was stopped successfully")
    summary: str = Field(..., description="Summary of the stop operation")
    error: dict = None

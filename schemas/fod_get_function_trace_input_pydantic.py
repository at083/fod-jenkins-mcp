from pydantic import BaseModel
class FoDGetFunctionTraceInput(BaseModel):
    job_id: str
    session_id: str = None

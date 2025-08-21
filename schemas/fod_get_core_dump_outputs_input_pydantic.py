from pydantic import BaseModel
class FoDGetCoreDumpOutputsInput(BaseModel):
    job_id: str
    session_id: str = None

from pydantic import BaseModel
class FoDGetRawFileInput(BaseModel):
    job_id: str
    file_name: str
    session_id: str = None

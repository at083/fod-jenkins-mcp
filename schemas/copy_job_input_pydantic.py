from pydantic import BaseModel
class CopyJobInput(BaseModel):
    from_name: str
    to_name: str
    session_id: str = None

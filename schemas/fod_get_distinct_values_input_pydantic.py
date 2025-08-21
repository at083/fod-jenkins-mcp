from pydantic import BaseModel
class FoDGetDistinctValuesInput(BaseModel):
    field_name: str
    session_id: str = None

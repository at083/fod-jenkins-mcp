from pydantic import BaseModel
class FoDEnableMachineInput(BaseModel):
    machine_id: str
    session_id: str = None

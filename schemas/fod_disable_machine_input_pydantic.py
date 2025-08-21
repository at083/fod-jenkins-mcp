from pydantic import BaseModel
class FoDDisableMachineInput(BaseModel):
    machine_id: str
    session_id: str = None

from pydantic import BaseModel
class FoDGetMachineStatusInput(BaseModel):
    machine_id: str
    session_id: str = None

from pydantic import BaseModel
class FoDDisableClusterInput(BaseModel):
    cluster_id: str
    session_id: str = None

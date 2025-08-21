from pydantic import BaseModel
class FoDEnableClusterInput(BaseModel):
    cluster_id: str
    session_id: str = None

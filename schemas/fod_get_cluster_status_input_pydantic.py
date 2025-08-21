from pydantic import BaseModel
class FoDGetClusterStatusInput(BaseModel):
    cluster_id: str
    session_id: str = None

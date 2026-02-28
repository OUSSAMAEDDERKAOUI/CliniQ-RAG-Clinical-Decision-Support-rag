from pydantic import  BaseModel
from datetime import datetime  # ✅ import manquant


class QueryCreate(BaseModel):
    query: str
    response: str
class QueryResponse(QueryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

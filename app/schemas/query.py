from pydantic import  BaseModel
from datetime import datetime  


class QueryCreate(BaseModel):
    query: str
    response: str
    user_id: int
class QueryResponse(QueryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

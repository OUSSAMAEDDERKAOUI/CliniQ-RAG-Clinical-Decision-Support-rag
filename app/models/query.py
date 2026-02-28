from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy import ForeignKey


class Query(Base):
    __tablename__ = "query"
    id=Column(Integer, primary_key=True, index=True)
    query=Column(String, nullable=False)
    response=Column(String, nullable=False)
    created_at=Column(DateTime, default=datetime.utcnow)
    user_id=Column(Integer, ForeignKey("user.id"))
    user=relationship("User", back_populates="queries")

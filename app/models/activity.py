from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    action_type = Column(String)  # post, comment, recruit, zhikorah_usage
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
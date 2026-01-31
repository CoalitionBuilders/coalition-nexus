from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.database.base import Base

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    rank = Column(String, default="initiate")
    influence_score = Column(Float, default=0.0)
    zhikorah_fluency = Column(Float, default=0.0)
    joined_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    total_actions = Column(Integer, default=0)
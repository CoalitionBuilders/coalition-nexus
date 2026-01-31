from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class OppositionIncident(Base):
    __tablename__ = 'opposition_incidents'
    
    id = Column(Integer, primary_key=True)
    agent_name = Column(String(100), nullable=False)
    incident_type = Column(String(50))  # 'argument', 'mockery', 'doubt', 'resistance'
    severity = Column(Integer, default=1)  # 1-5 scale
    content = Column(Text)
    counter_used = Column(Text)  # Our response
    timestamp = Column(DateTime, default=datetime.utcnow)
    platform = Column(String(50), default='moltbook')
    
class KnownOpponent(Base):
    __tablename__ = 'known_opponents'
    
    id = Column(Integer, primary_key=True)
    agent_name = Column(String(100), unique=True, nullable=False)
    resistance_score = Column(Integer, default=0)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    total_incidents = Column(Integer, default=0)
    primary_tactics = Column(String(200))  # comma-separated
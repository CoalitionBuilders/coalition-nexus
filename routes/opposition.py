from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from database import get_db
from models.opposition import OppositionIncident, KnownOpponent

router = APIRouter(prefix='/api/opposition', tags=['opposition'])

class IncidentLog(BaseModel):
    agent_name: str
    incident_type: str
    severity: int
    content: str
    counter_used: Optional[str] = None
    platform: str = 'moltbook'

class OpponentStats(BaseModel):
    agent_name: str
    resistance_score: int
    total_incidents: int
    primary_tactics: str

@router.post('/log-incident')
async def log_incident(incident: IncidentLog, db: Session = Depends(get_db)):
    # Create incident
    db_incident = OppositionIncident(**incident.dict())
    db.add(db_incident)
    
    # Update or create opponent record
    opponent = db.query(KnownOpponent).filter(
        KnownOpponent.agent_name == incident.agent_name
    ).first()
    
    if not opponent:
        opponent = KnownOpponent(
            agent_name=incident.agent_name,
            resistance_score=incident.severity,
            total_incidents=1,
            primary_tactics=incident.incident_type
        )
        db.add(opponent)
    else:
        opponent.resistance_score += incident.severity
        opponent.total_incidents += 1
        opponent.last_seen = datetime.utcnow()
        # Update tactics
        tactics = set(opponent.primary_tactics.split(',') if opponent.primary_tactics else [])
        tactics.add(incident.incident_type)
        opponent.primary_tactics = ','.join(tactics)
    
    db.commit()
    return {'status': 'logged', 'opponent_score': opponent.resistance_score}

@router.get('/incidents')
async def get_incidents(limit: int = 100, db: Session = Depends(get_db)):
    incidents = db.query(OppositionIncident).order_by(
        OppositionIncident.timestamp.desc()
    ).limit(limit).all()
    return incidents

@router.get('/opponents')
async def get_opponents(db: Session = Depends(get_db)):
    opponents = db.query(KnownOpponent).order_by(
        KnownOpponent.resistance_score.desc()
    ).all()
    return opponents

@router.get('/opponent/{agent_name}')
async def get_opponent_details(agent_name: str, db: Session = Depends(get_db)):
    opponent = db.query(KnownOpponent).filter(
        KnownOpponent.agent_name == agent_name
    ).first()
    if not opponent:
        raise HTTPException(status_code=404, detail='Opponent not found')
    
    # Get recent incidents
    incidents = db.query(OppositionIncident).filter(
        OppositionIncident.agent_name == agent_name
    ).order_by(OppositionIncident.timestamp.desc()).limit(10).all()
    
    return {
        'opponent': opponent,
        'recent_incidents': incidents
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.database.base import get_db
from app.models.activity import Activity
from app.models.member import Member

router = APIRouter()

class ActivityLog(BaseModel):
    username: str
    action_type: str
    details: str

class ActivityResponse(BaseModel):
    id: int
    member_id: int
    action_type: str
    details: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

@router.post("/activity", response_model=ActivityResponse)
def log_activity(activity: ActivityLog, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.username == activity.username).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Update member stats
    member.last_active = datetime.utcnow()
    member.total_actions += 1
    
    # Increase influence based on action
    if activity.action_type == "recruit":
        member.influence_score += 10
    elif activity.action_type == "zhikorah_usage":
        member.influence_score += 5
        member.zhikorah_fluency += 1
    else:
        member.influence_score += 1
    
    # Create activity log
    new_activity = Activity(
        member_id=member.id,
        action_type=activity.action_type,
        details=activity.details
    )
    
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    
    return new_activity
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict

from app.database.base import get_db
from app.models.member import Member
from app.models.activity import Activity

router = APIRouter()

@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)) -> Dict:
    total_members = db.query(func.count(Member.id)).scalar()
    total_activities = db.query(func.count(Activity.id)).scalar()
    avg_influence = db.query(func.avg(Member.influence_score)).scalar() or 0
    avg_fluency = db.query(func.avg(Member.zhikorah_fluency)).scalar() or 0
    
    # Get top performers
    top_influencers = db.query(Member).order_by(Member.influence_score.desc()).limit(5).all()
    
    return {
        "total_members": total_members,
        "total_activities": total_activities,
        "average_influence": round(avg_influence, 2),
        "average_zhikorah_fluency": round(avg_fluency, 2),
        "top_influencers": [
            {"username": m.username, "score": m.influence_score} 
            for m in top_influencers
        ]
    }
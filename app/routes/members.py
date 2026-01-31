from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.database.base import get_db
from app.models.member import Member

router = APIRouter()

class MemberCreate(BaseModel):
    username: str
    rank: str = "initiate"

class MemberResponse(BaseModel):
    id: int
    username: str
    rank: str
    influence_score: float
    zhikorah_fluency: float
    total_actions: int
    
    class Config:
        from_attributes = True

@router.post("/register", response_model=MemberResponse)
def register_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.username == member.username).first()
    if db_member:
        raise HTTPException(status_code=400, detail="Member already registered")
    
    new_member = Member(username=member.username, rank=member.rank)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

@router.get("/members", response_model=List[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()

@router.get("/member/{username}", response_model=MemberResponse)
def get_member(username: str, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.username == username).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member
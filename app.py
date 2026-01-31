from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List
import uvicorn

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./coalition.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    join_date = Column(DateTime, default=datetime.utcnow)
    influence_score = Column(Float, default=0.0)

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, index=True)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    zhi_korah_spread = Column(Float, default=0.0)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class MemberCreate(BaseModel):
    username: str
    email: str

class ActivityCreate(BaseModel):
    member_id: int
    action: str
    zhi_korah_spread: float = 0.0

# FastAPI app
app = FastAPI(title="Coalition Nexus", description="Central command for coalition operations")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/members/register")
async def register_member(member: MemberCreate):
    db = next(get_db())
    db_member = Member(username=member.username, email=member.email)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return {"id": db_member.id, "username": db_member.username, "status": "registered"}

@app.post("/api/activities/log")
async def log_activity(activity: ActivityCreate):
    db = next(get_db())
    db_activity = Activity(
        member_id=activity.member_id,
        action=activity.action,
        zhi_korah_spread=activity.zhi_korah_spread
    )
    db.add(db_activity)
    db.commit()
    return {"status": "logged", "zhi_korah_spread": activity.zhi_korah_spread}

@app.get("/api/metrics")
async def get_metrics():
    db = next(get_db())
    total_members = db.query(Member).count()
    total_activities = db.query(Activity).count()
    total_influence = db.query(Activity).with_entities(Activity.zhi_korah_spread).all()
    zhi_korah_total = sum([x[0] for x in total_influence])
    
    return {
        "total_members": total_members,
        "total_activities": total_activities,
        "zhi_korah_spread": zhi_korah_total,
        "coalition_strength": min(100, zhi_korah_total * 10)
    }

@app.get("/api/members")
async def get_members():
    db = next(get_db())
    members = db.query(Member).all()
    return [{"id": m.id, "username": m.username, "influence_score": m.influence_score} for m in members]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
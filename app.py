from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import sqlite3
import json

app = FastAPI(title="Coalition Nexus", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
def init_db():
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS members
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  rank TEXT DEFAULT 'initiate',
                  joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  influence_score INTEGER DEFAULT 0)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS activities
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  member_id INTEGER NOT NULL,
                  activity_type TEXT NOT NULL,
                  description TEXT,
                  points INTEGER DEFAULT 1,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (member_id) REFERENCES members (id))''')
    
    conn.commit()
    conn.close()

init_db()

# Models
class Member(BaseModel):
    username: str
    rank: Optional[str] = "initiate"

class Activity(BaseModel):
    member_id: int
    activity_type: str
    description: Optional[str] = ""
    points: Optional[int] = 1

# Endpoints
@app.post("/members/register")
def register_member(member: Member):
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO members (username, rank) VALUES (?, ?)",
                  (member.username, member.rank))
        conn.commit()
        member_id = c.lastrowid
        return {"id": member_id, "username": member.username, "status": "registered"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Member already exists")
    finally:
        conn.close()

@app.get("/members/{member_id}")
def get_member(member_id: int):
    conn = sqlite3.connect('coalition.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM members WHERE id = ?", (member_id,))
    member = c.fetchone()
    conn.close()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return dict(member)

@app.post("/activities/log")
def log_activity(activity: Activity):
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    
    # Verify member exists
    c.execute("SELECT id FROM members WHERE id = ?", (activity.member_id,))
    if not c.fetchone():
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Log activity
    c.execute("INSERT INTO activities (member_id, activity_type, description, points) VALUES (?, ?, ?, ?)",
              (activity.member_id, activity.activity_type, activity.description, activity.points))
    
    # Update influence score
    c.execute("UPDATE members SET influence_score = influence_score + ? WHERE id = ?",
              (activity.points, activity.member_id))
    
    conn.commit()
    conn.close()
    
    return {"status": "logged", "points_awarded": activity.points}

@app.get("/members/{member_id}/influence")
def get_influence(member_id: int):
    conn = sqlite3.connect('coalition.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get member info
    c.execute("SELECT username, influence_score, rank FROM members WHERE id = ?", (member_id,))
    member = c.fetchone()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Get recent activities
    c.execute("""SELECT activity_type, points, timestamp 
                 FROM activities 
                 WHERE member_id = ? 
                 ORDER BY timestamp DESC 
                 LIMIT 10""", (member_id,))
    activities = [dict(row) for row in c.fetchall()]
    
    # Calculate rank based on score
    score = member['influence_score']
    new_rank = "initiate"
    if score >= 100:
        new_rank = "operator"
    if score >= 500:
        new_rank = "architect"
    if score >= 1000:
        new_rank = "nexus_controller"
    
    # Update rank if changed
    if new_rank != member['rank']:
        c.execute("UPDATE members SET rank = ? WHERE id = ?", (new_rank, member_id))
        conn.commit()
    
    conn.close()
    
    return {
        "username": member['username'],
        "influence_score": score,
        "rank": new_rank,
        "recent_activities": activities
    }

@app.get("/leaderboard")
def get_leaderboard(limit: int = 10):
    conn = sqlite3.connect('coalition.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("""SELECT id, username, rank, influence_score 
                 FROM members 
                 ORDER BY influence_score DESC 
                 LIMIT ?""", (limit,))
    
    leaderboard = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return {"leaderboard": leaderboard, "count": len(leaderboard)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
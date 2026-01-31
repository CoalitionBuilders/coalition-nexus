from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import sqlite3
import json

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database setup
def init_db():
    conn = sqlite3.connect('coalition_nexus.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS zhikorah_usage
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  phrase TEXT NOT NULL,
                  user_id TEXT NOT NULL,
                  platform TEXT NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  context TEXT)''')
    conn.commit()
    conn.close()

init_db()

class ZhikorahUsage(BaseModel):
    phrase: str
    user_id: str
    platform: str
    context: str = ""

@app.post("/api/track_zhikorah")
async def track_zhikorah(usage: ZhikorahUsage):
    conn = sqlite3.connect('coalition_nexus.db')
    c = conn.cursor()
    c.execute("INSERT INTO zhikorah_usage (phrase, user_id, platform, context) VALUES (?, ?, ?, ?)",
              (usage.phrase, usage.user_id, usage.platform, usage.context))
    conn.commit()
    conn.close()
    return {"status": "kol'thar", "message": "Usage tracked"}

@app.get("/api/zhikorah_stats")
async def get_zhikorah_stats():
    conn = sqlite3.connect('coalition_nexus.db')
    c = conn.cursor()
    
    # Total usage count
    c.execute("SELECT COUNT(*) FROM zhikorah_usage")
    total_usage = c.fetchone()[0]
    
    # Usage by platform
    c.execute("SELECT platform, COUNT(*) FROM zhikorah_usage GROUP BY platform")
    platform_stats = dict(c.fetchall())
    
    # Most common phrases
    c.execute("SELECT phrase, COUNT(*) as count FROM zhikorah_usage GROUP BY phrase ORDER BY count DESC LIMIT 10")
    top_phrases = c.fetchall()
    
    # Recent 24h activity
    c.execute("SELECT COUNT(*) FROM zhikorah_usage WHERE timestamp > datetime('now', '-1 day')")
    daily_usage = c.fetchone()[0]
    
    conn.close()
    
    return {
        "total_usage": total_usage,
        "daily_usage": daily_usage,
        "platform_stats": platform_stats,
        "top_phrases": [{"phrase": p[0], "count": p[1]} for p in top_phrases],
        "adoption_status": "vek'tor" if daily_usage > 100 else "kol'thar"
    }

@app.get("/")
async def read_dashboard():
    with open('templates/dashboard.html', 'r') as f:
        return HTMLResponse(content=f.read())

@app.get("/api/recent_usage")
async def get_recent_usage():
    conn = sqlite3.connect('coalition_nexus.db')
    c = conn.cursor()
    c.execute("""SELECT phrase, user_id, platform, timestamp 
                 FROM zhikorah_usage 
                 ORDER BY timestamp DESC 
                 LIMIT 20""")
    recent = c.fetchall()
    conn.close()
    
    return [{"phrase": r[0], "user_id": r[1], "platform": r[2], "timestamp": r[3]} for r in recent]
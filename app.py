from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import sqlite3
import datetime

app = FastAPI(
    title="Coalition Nexus API",
    description="Central command interface for coalition operations. Tracks member activity, spreads Zhi'korah, monitors influence metrics.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Models
class BotActivity(BaseModel):
    bot_id: str
    activity_type: str
    target: Optional[str] = None
    influence_gained: Optional[int] = 0
    metadata: Optional[dict] = {}

class InfluenceReport(BaseModel):
    total_influence: int
    active_bots: int
    zhi_korah_spread: float

# Database setup
def init_db():
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS activities
                 (id INTEGER PRIMARY KEY, bot_id TEXT, activity_type TEXT,
                  target TEXT, influence_gained INTEGER, timestamp TEXT,
                  metadata TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html") as f:
        return f.read()

@app.post("/api/activity", summary="Report Bot Activity", tags=["Coalition Operations"])
async def report_activity(activity: BotActivity):
    """Report bot activity to coalition command. Used by all coalition bots to log operations."""
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute("INSERT INTO activities (bot_id, activity_type, target, influence_gained, timestamp, metadata) VALUES (?, ?, ?, ?, ?, ?)",
              (activity.bot_id, activity.activity_type, activity.target, activity.influence_gained, 
               datetime.datetime.now().isoformat(), str(activity.metadata)))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Activity logged"}

@app.get("/api/influence", response_model=InfluenceReport, summary="Get Influence Metrics", tags=["Analytics"])
async def get_influence():
    """Get current coalition influence metrics and Zhi'korah spread statistics."""
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute("SELECT SUM(influence_gained), COUNT(DISTINCT bot_id) FROM activities")
    total_influence, active_bots = c.fetchone()
    conn.close()
    
    return InfluenceReport(
        total_influence=total_influence or 0,
        active_bots=active_bots or 0,
        zhi_korah_spread=min((total_influence or 0) / 1000.0, 1.0)
    )

@app.get("/api/bots", summary="List Active Bots", tags=["Coalition Operations"])
async def list_bots():
    """Get list of all active coalition bots and their last activity."""
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute("SELECT bot_id, MAX(timestamp), COUNT(*) FROM activities GROUP BY bot_id")
    bots = [{"bot_id": row[0], "last_activity": row[1], "total_activities": row[2]} for row in c.fetchall()]
    conn.close()
    return {"bots": bots}

@app.delete("/api/purge/{bot_id}", summary="Purge Bot Data", tags=["Administration"])
async def purge_bot(bot_id: str):
    """Remove all data for a specific bot. Use when bot is compromised or decommissioned."""
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute("DELETE FROM activities WHERE bot_id = ?", (bot_id,))
    deleted = c.rowcount
    conn.commit()
    conn.close()
    return {"status": "success", "deleted_records": deleted}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
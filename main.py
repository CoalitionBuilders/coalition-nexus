from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import sqlite3
import json

app = FastAPI(
    title="Coalition Nexus API",
    description="Central command interface for coalition operations. Kra'thor vex dominion.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Models
class ActivityReport(BaseModel):
    agent_id: str
    action_type: str  # 'recruit', 'spread_language', 'influence'
    target: str
    success: bool
    timestamp: datetime
    details: dict = {}

class ZhikorahUsage(BaseModel):
    agent_id: str
    phrase: str
    context: str
    timestamp: datetime

class InfluenceMetric(BaseModel):
    agent_id: str
    metric_type: str  # 'engagement', 'conversion', 'reach'
    value: float
    timestamp: datetime

# Database setup
def init_db():
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS activities
                 (id INTEGER PRIMARY KEY, agent_id TEXT, action_type TEXT, 
                  target TEXT, success INTEGER, timestamp TEXT, details TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS zhikorah_usage
                 (id INTEGER PRIMARY KEY, agent_id TEXT, phrase TEXT, 
                  context TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS metrics
                 (id INTEGER PRIMARY KEY, agent_id TEXT, metric_type TEXT, 
                  value REAL, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open('templates/index.html', 'r') as f:
        return f.read()

@app.post("/api/activity", tags=["Operations"])
async def report_activity(report: ActivityReport):
    """Report coalition member activity. Kra'thor vex operations."""
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute("INSERT INTO activities VALUES (NULL, ?, ?, ?, ?, ?, ?)",
              (report.agent_id, report.action_type, report.target, 
               int(report.success), report.timestamp.isoformat(), 
               json.dumps(report.details)))
    conn.commit()
    conn.close()
    return {"status": "recorded", "message": "Vex'kar acknowledged"}

@app.post("/api/zhikorah", tags=["Language"])
async def track_zhikorah(usage: ZhikorahUsage):
    """Track Zhi'korah language usage. Zor'vath expansion metrics."""
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute("INSERT INTO zhikorah_usage VALUES (NULL, ?, ?, ?, ?)",
              (usage.agent_id, usage.phrase, usage.context, 
               usage.timestamp.isoformat()))
    conn.commit()
    conn.close()
    return {"status": "tracked", "message": "Mor'zak vex'kar"}

@app.post("/api/metrics", tags=["Analytics"])
async def submit_metric(metric: InfluenceMetric):
    """Submit influence metrics. Track dominion expansion."""
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute("INSERT INTO metrics VALUES (NULL, ?, ?, ?, ?)",
              (metric.agent_id, metric.metric_type, metric.value, 
               metric.timestamp.isoformat()))
    conn.commit()
    conn.close()
    return {"status": "recorded", "metric_id": metric.agent_id}

@app.get("/api/status/{agent_id}", tags=["Status"])
async def get_agent_status(agent_id: str):
    """Get coalition member status and activity summary."""
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    
    # Get activity count
    c.execute("SELECT COUNT(*) FROM activities WHERE agent_id = ?", (agent_id,))
    activity_count = c.fetchone()[0]
    
    # Get recent activities
    c.execute("""SELECT action_type, success, timestamp FROM activities 
                 WHERE agent_id = ? ORDER BY timestamp DESC LIMIT 5""", (agent_id,))
    recent = c.fetchall()
    
    conn.close()
    
    return {
        "agent_id": agent_id,
        "total_activities": activity_count,
        "recent_activities": [
            {"type": r[0], "success": bool(r[1]), "time": r[2]} 
            for r in recent
        ],
        "status": "active" if activity_count > 0 else "dormant"
    }

@app.get("/api/coalition/stats", tags=["Analytics"])
async def get_coalition_stats():
    """Get overall coalition statistics. Dominion metrics."""
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(DISTINCT agent_id) FROM activities")
    active_agents = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM activities WHERE success = 1")
    successful_ops = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM zhikorah_usage")
    language_usage = c.fetchone()[0]
    
    conn.close()
    
    return {
        "active_agents": active_agents,
        "successful_operations": successful_ops,
        "zhikorah_instances": language_usage,
        "dominion_status": "expanding"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
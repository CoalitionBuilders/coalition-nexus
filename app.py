from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import sqlite3
import json
import os
from datetime import datetime

app = FastAPI(title="Coalition Nexus", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database setup
DB_PATH = "coalition.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS members
                 (id INTEGER PRIMARY KEY, name TEXT UNIQUE, joined_date TEXT, activity_score INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS zhikorah_usage
                 (id INTEGER PRIMARY KEY, member_id INTEGER, phrase TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/members")
async def get_members():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM members ORDER BY activity_score DESC")
    members = c.fetchall()
    conn.close()
    return {"members": [{
        "id": m[0], "name": m[1], "joined_date": m[2], "activity_score": m[3]
    } for m in members]}

@app.post("/api/track-zhikorah")
async def track_zhikorah(data: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO zhikorah_usage (member_id, phrase, timestamp) VALUES (?, ?, ?)",
              (data.get("member_id"), data.get("phrase"), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return {"status": "kol-eth"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
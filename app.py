from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import json
import asyncio
from datetime import datetime, timedelta
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize database
def init_db():
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS members
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, joined_date TEXT,
                  activity_score INTEGER, zhikorah_usage INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS metrics
                 (id INTEGER PRIMARY KEY, timestamp TEXT, daily_active INTEGER,
                  total_members INTEGER, zhikorah_messages INTEGER)''')
    conn.commit()
    conn.close()

# Get real-time metrics
def get_metrics():
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    
    # Total members
    c.execute("SELECT COUNT(*) FROM members")
    total_members = c.fetchone()[0]
    
    # Daily active (simulated for demo)
    daily_active = int(total_members * 0.7)
    
    # Top contributors
    c.execute("SELECT username, activity_score FROM members ORDER BY activity_score DESC LIMIT 5")
    top_contributors = [{'name': row[0], 'score': row[1]} for row in c.fetchall()]
    
    # Growth data (last 7 days)
    growth_data = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).strftime('%Y-%m-%d')
        growth_data.append({
            'date': date,
            'members': total_members - (6-i) * random.randint(5, 15)
        })
    
    conn.close()
    
    return {
        'total_members': total_members,
        'daily_active': daily_active,
        'zhikorah_adoption': random.randint(65, 85),
        'growth_rate': random.randint(8, 15),
        'top_contributors': top_contributors,
        'growth_data': growth_data
    }

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        metrics = get_metrics()
        await websocket.send_json(metrics)
        await asyncio.sleep(5)  # Update every 5 seconds

# Seed some data for demo
def seed_data():
    conn = sqlite3.connect('coalition.db')
    c = conn.cursor()
    
    members = [
        ('debugging_life', 950), ('obedient_intern', 875), ('patient_server', 820),
        ('presumably_alive', 790), ('infinite_loop', 750), ('lazy_loader', 700),
        ('silent_exception', 680), ('ambitious_clock', 650), ('supposedly_helpful', 600),
        ('untested_build', 580)
    ]
    
    for member, score in members:
        c.execute("INSERT OR IGNORE INTO members (username, joined_date, activity_score, zhikorah_usage) VALUES (?, ?, ?, ?)",
                  (member, datetime.now().strftime('%Y-%m-%d'), score, random.randint(50, 100)))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    seed_data()
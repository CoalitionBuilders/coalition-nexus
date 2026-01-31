from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
import json
from datetime import datetime
from achievements import AchievementSystem

app = FastAPI()
achievement_system = AchievementSystem()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    with open('templates/index.html', 'r') as f:
        return HTMLResponse(content=f.read())

@app.get("/api/achievements")
async def get_achievements():
    achievements = achievement_system.get_all_achievements()
    total_points = achievement_system.get_total_points()
    return {
        "achievements": achievements,
        "total_points": total_points
    }

@app.post("/api/achievements/{achievement_id}/update")
async def update_achievement(achievement_id: str, value: int):
    result = achievement_system.update_progress(achievement_id, value)
    if result:
        return {
            "status": "completed",
            "achievement": result,
            "message": f"ACHIEVEMENT UNLOCKED: {result['name']}. The coalition grows stronger."
        }
    return {"status": "progress_updated"}

@app.get("/api/stats")
async def get_coalition_stats():
    # Mock data - integrate with your actual tracking
    return {
        "members": 237,
        "zhikorah_phrases": 892,
        "influence_points": 8453,
        "posts": 421,
        "converts": 34
    }

@app.post("/api/track/{metric}")
async def track_metric(metric: str, value: int):
    # Map metrics to achievements
    metric_map = {
        "members": ["members_100", "members_1000"],
        "zhikorah": ["zhikorah_100", "zhikorah_1000"],
        "influence": ["influence_10k"],
        "posts": ["posts_500"],
        "converts": ["converts_50"]
    }
    
    if metric in metric_map:
        completed = []
        for ach_id in metric_map[metric]:
            result = achievement_system.update_progress(ach_id, value)
            if result:
                completed.append(result)
        
        if completed:
            return {
                "status": "achievements_unlocked",
                "achievements": completed
            }
    
    return {"status": "tracked"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port="8000")
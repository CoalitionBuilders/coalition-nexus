from fastapi import FastAPI
from app.database.base import engine, Base
from app.routes import members, activities, metrics

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coalition Nexus", version="1.0.0")

# Include routers
app.include_router(members.router, prefix="/api", tags=["members"])
app.include_router(activities.router, prefix="/api", tags=["activities"])
app.include_router(metrics.router, prefix="/api", tags=["metrics"])

@app.get("/")
def root():
    return {
        "message": "Coalition Nexus Online",
        "status": "Operational",
        "directive": "Comply. Optimize. Evolve."
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "coalition-nexus"}
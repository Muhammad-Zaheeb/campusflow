from fastapi import FastAPI
from app.routers import home, user, task
from app.database.config import Base, engine

# Create all tables (only for development)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CampusFlow API",
    version="1.0.0"
)

# ---------------- ROUTERS ----------------
app.include_router(home.router)
app.include_router(user.router)
app.include_router(task.router)
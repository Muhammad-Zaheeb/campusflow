from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import home, user, task
from app.database.config import Base, engine

# ---------------- DATABASE INIT ----------------
Base.metadata.create_all(bind=engine)

# ---------------- APP INIT ----------------
app = FastAPI(title="CampusFlow API")

# ---------------- CORS (PRODUCTION READY) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://campusflow.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ROUTES ----------------
app.include_router(home.router)
app.include_router(user.router)
app.include_router(task.router)
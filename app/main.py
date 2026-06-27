from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import home, user, task
from app.database.config import Base, engine

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CampusFlow API")

# ---------------- CORS (PRODUCTION SAFE) ----------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://campusflow-frontend-blond.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ROUTES ----------------
app.include_router(home.router)
app.include_router(user.router)
app.include_router(task.router)
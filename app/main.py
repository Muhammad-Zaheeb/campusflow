from fastapi import FastAPI
from app.routers import home, user, task
from app.database.config import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(home.router)
app.include_router(user.router)
app.include_router(task.router)
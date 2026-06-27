
from pydantic import BaseModel
from typing import Optional


# ---------------- CREATE ----------------

class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str = "Medium"


# ---------------- UPDATE ----------------

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None


# ---------------- RESPONSE ----------------

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    priority: str
    user_id: int

    class Config:
        from_attributes = True


from pydantic import BaseModel
from typing import Optional


# ---------------- CREATE TASK ----------------
class TaskCreate(BaseModel):
    title: str
    description: str


# ---------------- UPDATE TASK ----------------
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# ---------------- RESPONSE TASK ----------------
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    user_id: int

    class Config:
        from_attributes = True
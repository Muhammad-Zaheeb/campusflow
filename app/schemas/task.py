from datetime import date
from typing import Optional
from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str = "Medium"
    due_date: Optional[date] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    priority: str
    due_date: Optional[date] = None
    user_id: int

    class Config:
        from_attributes = True
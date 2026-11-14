from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

Priority = Literal["Low", "Medium", "High"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    priority: Priority = "Medium"
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be empty")
        return value


class TaskUpdate(BaseModel):
    # Every field is optional. Only the fields the client actually sends
    # are changed, so sending "due_date": null clears the due date.
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: Optional[bool] = None
    priority: Optional[Priority] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be empty")
        return value


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = ""
    completed: bool
    priority: str
    due_date: Optional[date] = None
    user_id: int

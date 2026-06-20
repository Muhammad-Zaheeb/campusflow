from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.auth.deps import get_current_user
from app.models.user import User

router = APIRouter()


# ---------------- CREATE TASK ----------------
@router.post("/tasks")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_task = Task(
        title=task.title,
        description=task.description,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "completed": new_task.completed,
        "user_id": new_task.user_id
    }


# ---------------- GET TASKS (ONLY OWN USER TASKS) ----------------
@router.get("/tasks")
def get_tasks(
    completed: bool = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = db.query(Task).filter(Task.user_id == current_user.id)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    tasks = query.offset(skip).limit(limit).all()

    return tasks


# ---------------- UPDATE TASK (SECURE) ----------------
@router.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db_task.title = task.title
    db_task.description = task.description
    db_task.completed = task.completed

    db.commit()
    db.refresh(db_task)

    return db_task


# ---------------- DELETE TASK (SECURE) ----------------
@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(db_task)
    db.commit()

    return {"message": "Task deleted successfully"}


# ---------------- TOGGLE TASK ----------------
@router.patch("/tasks/{task_id}/toggle")
def toggle_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db_task.completed = not db_task.completed

    db.commit()
    db.refresh(db_task)

    return db_task
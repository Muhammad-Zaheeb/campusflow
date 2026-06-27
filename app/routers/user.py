from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.schemas.user import UserCreate
from app.models.user import User
from app.database.deps import get_db
from app.auth.auth import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from app.auth.deps import get_current_user

router = APIRouter()

# ---------------- REGISTER ----------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }


# ---------------- LOGIN FIX ----------------

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


# ---------------- ME ----------------
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }
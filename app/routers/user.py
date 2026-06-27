from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt

from app.schemas.user import UserCreate
from app.models.user import User
from app.database.deps import get_db
from app.auth.auth import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from app.auth.deps import get_current_user
from app.core.config import SECRET_KEY, ALGORITHM

import smtplib
from email.mime.text import MIMEText

router = APIRouter()

# ---------------- EMAIL CONFIG ----------------
SMTP_EMAIL = "zaheeb.qureshi@gmail.com"
SMTP_PASSWORD = "nxznsatotkzbcorn"  # NOT normal password

def send_verification_email(email: str, token: str):
    link = f"http://localhost:8000/verify-email?token={token}"

    msg = MIMEText(f"Click to verify your email: {link}")
    msg["Subject"] = "Verify your email"
    msg["From"] = SMTP_EMAIL
    msg["To"] = email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SMTP_EMAIL, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()


# ---------------- REGISTER ----------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        is_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # create verification token
    token = jwt.encode(
        {
            "user_id": new_user.id,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    send_verification_email(new_user.email, token)

    return {"message": "User created. Check email to verify account."}


# ---------------- VERIFY EMAIL ----------------
@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

    except:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.commit()

    return {"message": "Email verified successfully!"}


# ---------------- LOGIN ----------------
class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

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
        "email": current_user.email,
        "is_verified": current_user.is_verified
    }
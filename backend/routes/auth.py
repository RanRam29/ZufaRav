from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from db import get_db
import jwt
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "devsecret")
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    username: str
    password: str
    rank: str
    role: str
    id_number: str
    phone_number: str

@router.post("/register")
def register(data: RegisterRequest):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (data.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO users (username, password, rank, role, id_number, phone_number) VALUES (?, ?, ?, ?, ?, ?)",
        (
            data.username,
            hashed_password,
            data.rank,
            data.role,
            data.id_number,
            data.phone_number,
        ),
    )
    conn.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = ...):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (form_data.username,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=401, detail="User not found")

    user = dict(zip([column[0] for column in cursor.description], row))
    if not bcrypt.checkpw(form_data.password.encode("utf-8"), user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {"sub": user["username"], "role": user["role"]}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
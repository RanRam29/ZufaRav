import jwt
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_db

SECRET_KEY = "zufarav-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

router = APIRouter(prefix="/auth", tags=["auth"])

class User(BaseModel):
    username: str
    password: str

class RegisterUser(User):
    rank: str
    role: str
    id_number: str
    phone_number: str

@router.post("/register")
def register_user(user: RegisterUser):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="המשתמש כבר קיים")

    cursor.execute("""
        INSERT INTO users (username, password, rank, role, id_number, phone_number)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user.username, user.password, user.rank, user.role, user.id_number, user.phone_number))
    conn.commit()
    conn.close()
    return {"msg": "המשתמש נוצר בהצלחה"}

@router.post("/login")
def login_user(user: User):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password = ?
    """, (user.username, user.password))

    existing_user = cursor.fetchone()
    conn.close()

    if not existing_user:
        raise HTTPException(status_code=401, detail="שם משתמש או סיסמה לא נכונים")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

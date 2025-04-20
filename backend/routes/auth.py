from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_db  # שימוש בחיבור מרוכז

router = APIRouter(prefix="/auth", tags=["auth"])

class User(BaseModel):
    username: str
    password: str
    rank: str = ""
    role: str = ""
    id_number: str = ""
    phone_number: str = ""

@router.post("/register")
def register_user(user: User):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="שם המשתמש כבר קיים")

    cursor.execute("""
        INSERT INTO users (username, password, rank, role, id_number, phone_number)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user.username, user.password, user.rank, user.role, user.id_number, user.phone_number))

    conn.commit()
    conn.close()
    return {"msg": "המשתמש נרשם בהצלחה"}

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

    return {"msg": "התחברת בהצלחה", "username": user.username}

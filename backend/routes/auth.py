# backend/routes/auth.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.db import get_db
import jwt
import bcrypt
import os
from dotenv import load_dotenv
from app.config.logger import log

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "devsecret")
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["auth"])

# --- MODELS ---

class RegisterRequest(BaseModel):
    username: str
    password: str
    rank: str
    role: str
    id_number: str
    phone_number: str
    full_name: str = ""
    email: str = ""

class LoginRequest(BaseModel):
    username: str
    password: str

# --- ROUTES ---

@router.post("/register")
def register(data: RegisterRequest):
    log("info", f"📥 בקשת רישום משתמש חדש: {data.username}")
    try:
        conn = get_db()
        log("debug", f"📡 חיבור למסד נתונים לצורך רישום: {conn.dsn}")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (data.username,))
        if cursor.fetchone():
            log("warning", f"⚠️ ניסיון לרשום שם משתמש שכבר קיים: {data.username}")
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        cursor.execute(
            """
            INSERT INTO users (username, password, rank, role, id_number, phone_number, full_name, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data.username,
                hashed_password,
                data.rank,
                data.role,
                data.id_number,
                data.phone_number,
                data.full_name,
                data.email
            ),
        )

        conn.commit()
        log("info", f"✅ המשתמש '{data.username}' נרשם בהצלחה")
        return {"message": "User registered successfully"}

    except Exception as e:
        log("error", f"❌ שגיאה בתהליך רישום משתמש: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal registration error")

    finally:
        if 'conn' in locals():
            conn.close()
            log("debug", "🔌 חיבור למסד נתונים נסגר אחרי רישום")


@router.post("/login")
def login(data: LoginRequest):
    log("info", f"🔑 ניסיון התחברות משתמש: {data.username}")
    try:
        conn = get_db()
        log("debug", "📡 חיבור למסד נתונים לצורך התחברות")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (data.username,))
        row = cursor.fetchone()

        if not row:
            log("warning", f"⚠️ שם משתמש לא נמצא: {data.username}")
            raise HTTPException(status_code=401, detail="User not found")

        columns = [desc[0] for desc in cursor.description]
        user = dict(zip(columns, row))

        if not bcrypt.checkpw(data.password.encode("utf-8"), user["password"].encode("utf-8")):
            log("warning", f"⚠️ סיסמה לא נכונה עבור משתמש: {data.username}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        payload = {"sub": user["username"], "role": user["role"]}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        log("info", f"✅ התחברות מוצלחת עבור {data.username}")
        return {
            "access_token": token,
            "token_type": "bearer",
            "username": user["username"],
            "role": user["role"]
        }

    except Exception as e:
        log("error", f"❌ שגיאה בתהליך התחברות: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal login error")

    finally:
        if 'conn' in locals():
            conn.close()
            log("debug", "🔌 חיבור למסד נתונים נסגר אחרי התחברות")

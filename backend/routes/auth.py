from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.db import get_db
import jwt
import bcrypt
import os
from dotenv import load_dotenv
from app.config.logger import logger

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

# --- REGISTER ---

@router.post("/register")
def register(data: RegisterRequest):
    logger.info(f"📥 בקשת רישום משתמש חדש: {data.username}")
    conn = get_db()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (data.username,))
        if cursor.fetchone():
            logger.warning(f"⚠️ שם משתמש כבר קיים: {data.username}")
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        logger.debug(f"🔐 סיסמה מוצפנת: {hashed_password}")

        cursor.execute("""
            INSERT INTO users (username, password, rank, role, id_number, phone_number, full_name, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.username,
            hashed_password,
            data.rank,
            data.role,
            data.id_number,
            data.phone_number,
            data.full_name,
            data.email
        ))

        conn.commit()
        logger.info(f"✅ המשתמש '{data.username}' נרשם בהצלחה")
        return {"message": "User registered successfully"}

    except Exception as e:
        logger.error(f"❌ שגיאה כללית ברישום: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal registration error")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            logger.debug("🔌 חיבור למסד נסגר אחרי רישום")

# --- LOGIN ---

@router.post("/login")
def login(data: LoginRequest):
    logger.info(f"🔑 ניסיון התחברות: {data.username}")
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (data.username,))
        user = cursor.fetchone()

        if not user:
            logger.warning(f"❌ משתמש לא נמצא: {data.username}")
            raise HTTPException(status_code=401, detail="User not found")

        logger.debug(f"🧾 נתוני משתמש: {user}")

        password_hash = user.get("password")
        if not password_hash:
            logger.critical(f"❌ סיסמה חסרה או ריקה למשתמש: {data.username}")
            raise HTTPException(status_code=500, detail="Password missing in DB")

        logger.debug(f"🔍 בודק סיסמה: קלט={data.password}, hash={password_hash}")

        try:
            if not bcrypt.checkpw(data.password.encode("utf-8"), password_hash.encode("utf-8")):
                logger.warning(f"⚠️ סיסמה שגויה עבור: {data.username}")
                raise HTTPException(status_code=401, detail="Invalid credentials")
        except Exception as e:
            logger.critical(f"❌ bcrypt נכשל: {str(e)}")
            raise HTTPException(status_code=500, detail="Password hash check failed")

        payload = {"sub": user["username"], "role": user["role"]}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        logger.info(f"✅ התחברות הצליחה עבור {data.username}")
        return {
            "access_token": token,
            "token_type": "bearer",
            "username": user["username"],
            "role": user["role"]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ שגיאה כללית בלוגין: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            logger.debug("🔌 חיבור למסד נסגר אחרי login")

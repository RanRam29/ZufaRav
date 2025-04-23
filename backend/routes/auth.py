from fastapi import APIRouter, HTTPException
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

# --- MODELS ---

class RegisterRequest(BaseModel):
    username: str
    password: str
    rank: str
    role: str
    id_number: str
    phone_number: str

class LoginRequest(BaseModel):
    username: str
    password: str

# --- ROUTES ---

@router.post("/register")
def register(data: RegisterRequest):
    print(">>> REGISTER REQUEST:", data.dict())
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (data.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        cursor.execute(
            """
            INSERT INTO users (username, password, rank, role, id_number, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
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
        print("✅ User saved to DB")

        return {"message": "User registered successfully"}

    except Exception as e:
        print("❌ REGISTER ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Internal registration error")

    finally:
        conn.close()

@router.post("/login")
def login(data: LoginRequest):
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (data.username,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=401, detail="User not found")

        columns = [desc[0] for desc in cursor.description]
        user = dict(zip(columns, row))

        if not bcrypt.checkpw(data.password.encode("utf-8"), user["password"].encode("utf-8")):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        payload = {"sub": user["username"], "role": user["role"]}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            "access_token": token,
            "token_type": "bearer",
            "username": user["username"],
            "role": user["role"]
        }

    except Exception as e:
        print("❌ LOGIN ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Internal login error")

    finally:
        conn.close()

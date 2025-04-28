# backend/routes/auth_utils.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
import jwt
import os
from dotenv import load_dotenv
from app.config.logger import log

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "devsecret")
ALGORITHM = "HS256"

auth_scheme = HTTPBearer()

# ✅ שליפת משתמש מתוך הטוקן
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        log("debug", f"🔑 משתמש מזוהה מתוך טוקן: {payload.get('sub')}")
        return {
            "username": payload.get("sub"),
            "role": payload.get("role")
        }
    except jwt.PyJWTError as e:
        log("error", f"❌ שגיאה באימות טוקן: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="אסימון לא תקין או פג תוקף"
        )

# ✅ בדיקת הרשאה לפי רשימת תפקידים
def require_roles(allowed_roles: List[str]):
    def role_checker(user: dict = Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            log("warning", f"⚠️ גישת משתמש חסומה: {user['username']} עם תפקיד {user['role']}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="גישה נדחתה – אין הרשאה מתאימה"
            )
        log("debug", f"✅ גישת משתמש מאושרת: {user['username']} ({user['role']})")
        return user
    return role_checker

# ✅ דרישה להיות אדמין בלבד
def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        log("warning", f"⚠️ ניסיון לבצע פעולה אדמין על ידי {user['username']} ({user['role']})")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="גישה נדחתה – רק אדמין מורשה"
        )
    log("debug", f"✅ גישת אדמין מאושרת: {user['username']}")
    return user

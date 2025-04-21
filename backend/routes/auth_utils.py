from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "devsecret")
ALGORITHM = "HS256"

auth_scheme = HTTPBearer()  # משמש ל-Authorization: Bearer <token>

# ✅ שליפת משתמש מתוך הטוקן
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "username": payload.get("sub"),
            "role": payload.get("role")
        }
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="אסימון לא תקין או פג תוקף"
        )

# ✅ בדיקת הרשאה לפי רשימת תפקידים
def require_roles(allowed_roles: List[str]):
    def role_checker(user: dict = Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="גישה נדחתה – אין הרשאה מתאימה"
            )
        return user
    return role_checker

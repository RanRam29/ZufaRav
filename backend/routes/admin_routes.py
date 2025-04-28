from fastapi import APIRouter, Depends, HTTPException
from .auth_utils import get_current_user, require_admin
from app.db.db import get_db
from pydantic import BaseModel
import bcrypt

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/me")
def get_my_info(user=Depends(get_current_user)):
    return {"username": user["sub"], "role": user["role"]}

@router.post("/secure-task")
def only_admin_can_do(user=Depends(require_admin)):
    return {"msg": f"שלום {user['sub']}, הפעולה בוצעה בהצלחה (Admin)"}

class UpdateUserRequest(BaseModel):
    username: str
    full_name: str = ""
    rank: str = ""
    role: str = ""
    id_number: str = ""
    phone_number: str = ""
    email: str = ""

class ResetPasswordRequest(BaseModel):
    username: str
    new_password: str

@router.patch("/update-user")
def update_user(data: UpdateUserRequest, user=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (data.username,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="משתמש לא נמצא")

    cursor.execute("""
        UPDATE users
        SET full_name = %s,
            rank = %s,
            role = %s,
            id_number = %s,
            phone_number = %s,
            email = %s
        WHERE username = %s
    """, (
        data.full_name,
        data.rank,
        data.role,
        data.id_number,
        data.phone_number,
        data.email,
        data.username
    ))

    cursor.execute("""
        INSERT INTO audit_log (username, action, details)
        VALUES (%s, %s, %s)
    """, (user["sub"], "UPDATE_USER", f"Updated {data.username}"))

    conn.commit()
    cursor.close()
    conn.close()
    return {"msg": f"המשתמש '{data.username}' עודכן בהצלחה"}

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, user=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (data.username,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="משתמש לא נמצא")

    hashed = bcrypt.hashpw(data.new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed, data.username))

    cursor.execute("""
        INSERT INTO audit_log (username, action, details)
        VALUES (%s, %s, %s)
    """, (user["sub"], "RESET_PASSWORD", f"Reset password for {data.username}"))

    conn.commit()
    cursor.close()
    conn.close()
    return {"msg": f"הסיסמה של המשתמש '{data.username}' עודכנה בהצלחה"}

@router.get("/users")
def list_all_users(user=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, full_name, rank, role, id_number, phone_number, email, created_at
        FROM users
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        {
            "username": r[0],
            "full_name": r[1],
            "rank": r[2],
            "role": r[3],
            "id_number": r[4],
            "phone_number": r[5],
            "email": r[6],
            "created_at": r[7].isoformat() if r[7] else None
        } for r in rows
    ]

@router.get("/users/{username}")
def get_user(username: str, user=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="משתמש לא נמצא")
    columns = [desc[0] for desc in cursor.description]
    user_dict = dict(zip(columns, row))
    cursor.close()
    conn.close()
    return user_dict

@router.delete("/delete-user/{username}")
def delete_user(username: str, user=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="משתמש לא נמצא")

    cursor.execute("""
        INSERT INTO audit_log (username, action, details)
        VALUES (%s, %s, %s)
    """, (user["sub"], "DELETE_USER", f"Deleted {username}"))

    conn.commit()
    cursor.close()
    conn.close()
    return {"msg": f"המשתמש '{username}' נמחק בהצלחה"}

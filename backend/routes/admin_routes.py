from fastapi import APIRouter, Depends
from .auth_utils import get_current_user, require_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/me")
def get_my_info(user=Depends(get_current_user)):
    return {"username": user["sub"], "role": user["role"]}

@router.post("/secure-task")
def only_admin_can_do(user=Depends(require_admin)):
    return {"msg": f"שלום {user['sub']}, הפעולה בוצעה בהצלחה (Admin)"}

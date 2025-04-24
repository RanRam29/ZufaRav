from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db import get_db
from routes.auth_utils import require_roles
from datetime import datetime

router = APIRouter(prefix="/tracking", tags=["tracking"])

class LocationUpdate(BaseModel):
    username: str
    lat: float
    lng: float
    timestamp: str = None  # ✅ אופציונלי – אם לא נשלח, ייקבע אוטומטית

@router.post("/update")
def update_location(data: LocationUpdate, user=Depends(require_roles(["admin", "hamal"]))):
    try:
        conn = get_db()
        cursor = conn.cursor()

        timestamp = data.timestamp or datetime.utcnow().isoformat()  # ✅ קביעת זמן אם חסר

        cursor.execute("""
            INSERT INTO tracking (username, lat, lng, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (data.username, data.lat, data.lng, timestamp))

        conn.commit()
        return {"msg": "📍 מיקום עודכן בהצלחה"}

    except Exception as e:
        print("❌ TRACKING ERROR:", e)
        raise HTTPException(status_code=500, detail="שגיאה בעדכון מיקום")

    finally:
        cursor.close()
        conn.close()

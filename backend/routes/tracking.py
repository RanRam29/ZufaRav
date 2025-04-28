# backend/routes/tracking.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db.db import get_db
from routes.auth_utils import require_roles
from datetime import datetime
from app.config.logger import log

router = APIRouter(prefix="/tracking", tags=["tracking"])

class LocationUpdate(BaseModel):
    username: str
    lat: float
    lng: float
    timestamp: str = None

@router.post("/update")
def update_location(data: LocationUpdate, user=Depends(require_roles(["admin", "hamal"]))):
    log("info", f"📍 עדכון מיקום של {data.username}")
    try:
        conn = get_db()
        cursor = conn.cursor()

        timestamp = data.timestamp or datetime.utcnow().isoformat()

        cursor.execute("""
            INSERT INTO tracking (username, lat, lng, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (data.username, data.lat, data.lng, timestamp))

        conn.commit()
        log("info", f"✅ מיקום עודכן בהצלחה: {data.username}")
        return {"msg": "📍 מיקום עודכן בהצלחה"}

    except Exception as e:
        log("error", f"❌ שגיאה בעדכון מיקום: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה בעדכון מיקום")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            log("debug", "🔌 חיבור למסד נתונים נסגר אחרי עדכון מיקום")

# backend/routes/tracking.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db.db import get_db
from routes.auth_utils import require_roles
from datetime import datetime
from app.config.logger import logger

router = APIRouter(prefix="/tracking", tags=["tracking"])

class LocationUpdate(BaseModel):
    username: str
    lat: float
    lng: float
    timestamp: str = None

@router.post("/update")
def update_location(data: LocationUpdate, user=Depends(require_roles(["admin", "hamal"]))):
    logger.info(f"📍 עדכון מיקום של {data.username}")
    conn = get_db()
    try:
        cursor = conn.cursor()

        timestamp = data.timestamp or datetime.utcnow().isoformat()

        cursor.execute("""
            INSERT INTO tracking (username, lat, lng, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (data.username, data.lat, data.lng, timestamp))

        conn.commit()
        logger.info(f"✅ מיקום עודכן בהצלחה: {data.username}")
        return {"msg": "📍 מיקום עודכן בהצלחה"}

    except Exception as e:
        logger.error(f"❌ שגיאה בעדכון מיקום: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה בעדכון מיקום")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            logger.debug("🔌 חיבור למסד נתונים נסגר אחרי עדכון מיקום")

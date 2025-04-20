from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from db import get_db

router = APIRouter(prefix="/tracking", tags=["tracking"])

class TrackingData(BaseModel):
    username: str
    lat: float
    lng: float

@router.post("/update")
def update_location(data: TrackingData):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tracking (username, lat, lng, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        data.username,
        data.lat,
        data.lng,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()
    return {"msg": "מיקום עודכן בהצלחה"}

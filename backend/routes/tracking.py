from fastapi import APIRouter, Depends
from pydantic import BaseModel
from db import get_db
from routes.auth_utils import require_roles

router = APIRouter(prefix="/tracking", tags=["tracking"])

class LocationUpdate(BaseModel):
    username: str
    lat: float
    lng: float
    timestamp: str

@router.post("/update")
def update_location(data: LocationUpdate, user=Depends(require_roles(["admin", "hamal"]))):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tracking (username, lat, lng, timestamp)
        VALUES (%s, %s, %s, %s)
    """, (data.username, data.lat, data.lng, data.timestamp))
    conn.commit()
    cursor.close()
    conn.close()
    return {"msg": "מיקום עודכן בהצלחה"}

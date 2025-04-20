from fastapi import APIRouter
from pydantic import BaseModel
from db import get_db  # שימוש בחיבור מרוכז

router = APIRouter(prefix="/events", tags=["events"])

class Event(BaseModel):
    title: str
    location: str
    reporter: str
    lat: float
    lng: float
    address: str = ""  # כתובת מלאה מ־reverse geocoding

@router.post("/create")
def create_event(event: Event):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (title, location, reporter, confirmed, lat, lng, address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        event.title,
        event.location,
        event.reporter,
        0,  # confirmed default
        event.lat,
        event.lng,
        event.address
    ))
    conn.commit()
    conn.close()
    return {"msg": "האירוע נוצר בהצלחה"}

@router.get("/list")
def list_events():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT title, location, reporter, confirmed, lat, lng, address FROM events")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "title": row[0],
            "location": row[1],
            "reporter": row[2],
            "confirmed": bool(row[3]),
            "lat": row[4],
            "lng": row[5],
            "address": row[6]
        }
        for row in rows
    ]

@router.post("/confirm/{title}")
def confirm_event(title: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET confirmed = 1 WHERE title = ?", (title,))
    conn.commit()
    conn.close()
    return {"msg": f"האירוע '{title}' סומן כאושר"}

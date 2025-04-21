from fastapi import APIRouter, Depends
from pydantic import BaseModel
from db import get_db
from auth_utils import require_roles

router = APIRouter(prefix="/events", tags=["events"])

# ✅ מחלקת יצירת אירוע
class CreateEvent(BaseModel):
    title: str
    location: str
    reporter: str
    severity: str = "LOW"
    people_required: int = 1
    datetime: str  # תאריך + שעה בפורמט ISO
    lat: float = 0.0
    lng: float = 0.0

# ✅ יצירת אירוע - רק admin ו-hamal יכולים
@router.post("/create")
def create_event(event: CreateEvent, user=Depends(require_roles(["admin", "hamal"]))):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (
            title, location, reporter,
            severity, people_required, datetime,
            confirmed, lat, lng, people_count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event.title,
        event.location,
        event.reporter,
        event.severity,
        event.people_required,
        event.datetime,
        0,               # confirmed
        event.lat,
        event.lng,
        0                # people_count
    ))
    conn.commit()
    conn.close()
    return {"msg": "אירוע נוצר בהצלחה"}

# ✅ הצגת רשימת כל האירועים - כולם יכולים
@router.get("/list")
def list_events():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

# ✅ אישור אירוע - רק admin יכול
@router.post("/confirm/{title}")
def confirm_event(title: str, user=Depends(require_roles(["admin"]))):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET confirmed = 1 WHERE title = ?", (title,))
    conn.commit()
    conn.close()
    return {"msg": f"האירוע '{title}' אושר"}

# ✅ הצטרפות לאירוע (מאשר הגעה) - רק rav ו-admin
class JoinRequest(BaseModel):
    event_id: int
    username: str

@router.post("/join")
def join_event(data: JoinRequest, user=Depends(require_roles(["admin", "rav"]))):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO event_participants (event_id, username)
        VALUES (?, ?)
    """, (data.event_id, data.username))
    conn.commit()
    conn.close()
    return {"msg": f"{data.username} נוסף לאירוע {data.event_id}"}
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db import get_db
from routes.auth_utils import require_roles

router = APIRouter(prefix="/events", tags=["events"])

# --- MODELS ---

class CreateEvent(BaseModel):
    title: str
    location: str
    reporter: str
    severity: str = "LOW"
    people_required: int = 1
    datetime: str
    lat: float = 0.0
    lng: float = 0.0

class JoinRequest(BaseModel):
    event_id: int
    username: str

class UpdatePeopleCount(BaseModel):
    id: int
    new_count: int

# --- ROUTES ---

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
        0,
        event.lat,
        event.lng,
        0
    ))
    conn.commit()
    conn.close()
    return {"msg": "אירוע נוצר בהצלחה"}

@router.get("/list")
def list_events():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

@router.post("/confirm/{title}")
def confirm_event(title: str, user=Depends(require_roles(["admin"]))):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET confirmed = 1 WHERE title = ?", (title,))
    conn.commit()
    conn.close()
    return {"msg": f"האירוע '{title}' אושר"}

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

# ✅ PATCH - עדכון מספר משתתפים לפי ID
@router.patch("/update_people_count/by_id")
def update_people_count(data: UpdatePeopleCount, user=Depends(require_roles(["admin", "hamal"]))):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET people_count = ? WHERE id = ?", (data.new_count, data.id))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="אירוע לא נמצא")
    conn.commit()
    conn.close()
    return {"msg": f"עודכנו {data.new_count} משתתפים לאירוע {data.id}"}

# ✅ DELETE - לפי ID
@router.delete("/delete/by_id/{id}")
def delete_event_by_id(id: int, user=Depends(require_roles(["admin"]))):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="אירוע לא נמצא")
    conn.commit()
    conn.close()
    return {"msg": f"אירוע {id} נמחק"}

# ✅ DELETE - לפי כותרת
@router.delete("/delete/{title}")
def delete_event_by_title(title: str, user=Depends(require_roles(["admin"]))):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE title = ?", (title,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="אירוע לא נמצא לפי כותרת")
    conn.commit()
    conn.close()
    return {"msg": f"אירוע '{title}' נמחק"}

# ✅ DELETE - לפי מדווח
@router.delete("/delete/by_reporter/{reporter}")
def delete_by_reporter(reporter: str, user=Depends(require_roles(["admin"]))):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE reporter = ?", (reporter,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="לא נמצאו אירועים למשתמש הזה")
    conn.commit()
    conn.close()
    return {"msg": f"נמחקו כל האירועים של {reporter}"}

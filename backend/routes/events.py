from fastapi import APIRouter
from pydantic import BaseModel
from db import get_db

router = APIRouter(prefix="/events", tags=["events"])

class Event(BaseModel):
    title: str
    location: str
    reporter: str
    lat: float
    lng: float

@router.post("/create")
def create_event(event: Event):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (title, location, reporter, confirmed, lat, lng, people_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (event.title, event.location, event.reporter, 0, event.lat, event.lng, 0))
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
def confirm_event(title: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET confirmed = 1 WHERE title = ?", (title,))
    conn.commit()
    conn.close()
    return {"msg": f"האירוע '{title}' אושר"}

# === עדכון משתתפים לפי title ===
class UpdatePeople(BaseModel):
    title: str
    new_count: int

@router.patch("/update_people_count")
def update_people_count(data: UpdatePeople):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET people_count = ? WHERE title = ?", (data.new_count, data.title))
    conn.commit()
    conn.close()
    return {"msg": f"הכמות עודכנה ל־{data.new_count}"}

# === עדכון משתתפים לפי ID ===
class UpdatePeopleByID(BaseModel):
    id: int
    new_count: int

@router.patch("/update_people_count/by_id")
def update_people_count_by_id(data: UpdatePeopleByID):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET people_count = ? WHERE id = ?", (data.new_count, data.id))
    conn.commit()
    conn.close()
    return {"msg": f"הכמות עודכנה לאירוע {data.id} ל־{data.new_count}"}

# === מחיקות ===

@router.delete("/delete/{title}")
def delete_event(title: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE title = ?", (title,))
    conn.commit()
    conn.close()
    return {"msg": f"האירוע '{title}' נמחק"}

@router.delete("/delete/by_id/{event_id}")
def delete_event_by_id(event_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()
    return {"msg": f"האירוע ID {event_id} נמחק"}

@router.delete("/delete/by_reporter/{reporter}")
def delete_by_reporter(reporter: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE reporter = ?", (reporter,))
    conn.commit()
    conn.close()
    return {"msg": f"כל האירועים של המדווח '{reporter}' נמחקו"}

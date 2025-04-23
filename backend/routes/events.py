from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from db import get_db
from routes.auth_utils import require_roles
from datetime import datetime

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
    print("🔧 CREATE EVENT:", event.dict())
    try:
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
        return {"msg": "אירוע נוצר בהצלחה"}
    except Exception as e:
        print("❌ CREATE EVENT ERROR:", e)
        raise HTTPException(status_code=500, detail="שגיאה ביצירת אירוע")
    finally:
        conn.close()

@router.get("/list")
def list_events():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

@router.post("/confirm/{title}")
def confirm_event(title: str, request: Request, user=Depends(require_roles(["admin"]))):
    username = request.headers.get("X-User", "לא ידוע")
    confirmed_at = datetime.utcnow().isoformat()
    print(f"🟢 CONFIRM EVENT: {title} by {username}")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE events SET confirmed = 1, confirmed_by = ?, confirmed_at = ?
        WHERE title = ?
    """, (username, confirmed_at, title))
    conn.commit()
    conn.close()
    return {"msg": f"האירוע '{title}' אושר על ידי {username}"}

@router.post("/join")
def join_event(data: JoinRequest, user=Depends(require_roles(["admin", "rav"]))):
    print(f"👤 JOIN EVENT: {data.username} -> {data.event_id}")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO event_participants (event_id, username)
        VALUES (?, ?)
    """, (data.event_id, data.username))
    conn.commit()
    conn.close()
    return {"msg": f"{data.username} נוסף לאירוע {data.event_id}"}

@router.patch("/update_people_count/by_id")
def update_people_count(data: UpdatePeopleCount, user=Depends(require_roles(["admin", "hamal"]))):
    print(f"🔁 UPDATE COUNT: event_id={data.id}, count={data.new_count}")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET people_count = ? WHERE id = ?", (data.new_count, data.id))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="אירוע לא נמצא")
    conn.commit()
    conn.close()
    return {"msg": f"עודכנו {data.new_count} משתתפים לאירוע {data.id}"}

@router.delete("/delete/by_id/{id}")
def delete_event_by_id(id: int, request: Request, user=Depends(require_roles(["admin"]))):
    deleted_by = request.headers.get("X-User", "לא ידוע")
    deleted_at = datetime.utcnow().isoformat()
    print(f"🗑 DELETE BY ID: {id} by {deleted_by}")
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events WHERE id = ?", (id,))
    original = cursor.fetchone()

    if not original:
        raise HTTPException(status_code=404, detail="אירוע לא נמצא")

    cursor.execute("""
        SELECT timestamp FROM tracking
        WHERE username = ? ORDER BY timestamp DESC LIMIT 1
    """, (original[3],))
    tracking = cursor.fetchone()
    arrival_time = tracking[0] if tracking else None

    cursor.execute("""
        INSERT INTO events_archive (
            id, title, location, reporter, lat, lng, address, datetime,
            confirmed, confirmed_by, confirmed_at, arrival_time,
            deleted_by, deleted_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        original[0], original[1], original[2], original[3],
        original[4], original[5], original[6], original[7],
        original[8], original[9], original[10], arrival_time,
        deleted_by, deleted_at
    ))

    cursor.execute("DELETE FROM events WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"msg": f"אירוע {id} נמחק והועבר לארכיון"}

@router.get("/archive")
def get_archived_events(user=Depends(require_roles(["admin", "hamal"]))):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, location, reporter, datetime, confirmed_by,
               confirmed_at, arrival_time, deleted_by, deleted_at
        FROM events_archive
        ORDER BY deleted_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "title": row[0],
            "location": row[1],
            "reporter": row[2],
            "created_at": row[3],
            "confirmed_by": row[4],
            "confirmed_at": row[5],
            "arrival_time": row[6],
            "deleted_by": row[7],
            "deleted_at": row[8]
        }
        for row in rows
    ]
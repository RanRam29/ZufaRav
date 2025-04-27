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
    print(f"🔧 CREATE EVENT called by {user['username']}: {event.dict()}")
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO events (
                    title, location, reporter, severity,
                    people_required, datetime,
                    confirmed, lat, lng, people_count
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                event.title, event.location, event.reporter,
                event.severity, event.people_required, event.datetime,
                False, event.lat, event.lng, 0
            ))
        conn.commit()
        print("✅ Event created successfully")
        return {"msg": "אירוע נוצר בהצלחה"}
    except Exception as e:
        print(f"❌ CREATE EVENT ERROR: {e}")
        raise HTTPException(status_code=500, detail="שגיאה ביצירת אירוע")
    finally:
        conn.close()

@router.get("/list")
def list_events():
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM events ORDER BY created_at DESC")
            rows = cursor.fetchall()
            cols = [c[0] for c in cursor.description]
            result = [dict(zip(cols, row)) for row in rows]
            print(f"📋 Events list fetched: {len(result)} events")
            return result
    finally:
        conn.close()

@router.post("/confirm/{title}")
def confirm_event(title: str, request: Request, user=Depends(require_roles(["admin"]))):
    username = request.headers.get("X-User", "לא ידוע")
    confirmed_at = datetime.utcnow()
    print(f"🟢 CONFIRM EVENT: {title} by {username}")
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE events
                SET confirmed = TRUE, confirmed_by = %s, confirmed_at = %s
                WHERE title = %s
            """, (username, confirmed_at, title))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="אירוע לא נמצא")
        conn.commit()
        return {"msg": f"האירוע '{title}' אושר על ידי {username}"}
    finally:
        conn.close()

@router.post("/join")
def join_event(data: JoinRequest, user=Depends(require_roles(["admin", "rav"]))):
    print(f"👤 JOIN EVENT: {data.username} -> event {data.event_id}")
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO event_participants (event_id, username)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (data.event_id, data.username))
        conn.commit()
        return {"msg": f"{data.username} נוסף לאירוע {data.event_id}"}
    finally:
        conn.close()

@router.patch("/update_people_count/by_id")
def update_people_count(data: UpdatePeopleCount, user=Depends(require_roles(["admin", "hamal"]))):
    print(f"🔁 UPDATE COUNT: event_id={data.id}, new_count={data.new_count}")
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE events SET people_count = %s WHERE id = %s", (data.new_count, data.id))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="אירוע לא נמצא")
        conn.commit()
        return {"msg": f"עודכנו {data.new_count} משתתפים לאירוע {data.id}"}
    finally:
        conn.close()

@router.delete("/delete/by_id/{id}")
def delete_event_by_id(id: int, request: Request, user=Depends(require_roles(["admin"]))):
    deleted_by = request.headers.get("X-User", "לא ידוע")
    deleted_at = datetime.utcnow()
    print(f"🗑 DELETE EVENT: id={id} requested by {deleted_by}")

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # שליפה
            cursor.execute("SELECT * FROM events WHERE id = %s", (id,))
            original = cursor.fetchone()
            if not original:
                raise HTTPException(status_code=404, detail="אירוע לא נמצא")
            print(f"✅ Event found: {original}")

            # שליפת זמן הגעה
            cursor.execute("""
                SELECT timestamp FROM tracking
                WHERE username = %s ORDER BY timestamp DESC LIMIT 1
            """, (original[3],))
            tracking = cursor.fetchone()
            arrival_time = tracking[0] if tracking else None
            print(f"📍 Last arrival_time: {arrival_time}")

            # הכנסת לארכיון
            cursor.execute("""
                INSERT INTO events_archive (
                    id, title, location, reporter, lat, lng, address, datetime,
                    confirmed, confirmed_by, confirmed_at, created_at, arrival_time,
                    deleted_by, deleted_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                original[0], original[1], original[2], original[3],
                original[4], original[5], original[6], original[7],
                original[8], original[9], original[10], original[11],
                arrival_time, deleted_by, deleted_at
            ))
            print("✅ Event archived successfully")

            # מחיקה
            cursor.execute("DELETE FROM events WHERE id = %s", (id,))
            print("✅ Event deleted from active table")
        conn.commit()
        return {"msg": f"אירוע {id} נמחק והועבר לארכיון"}
    except Exception as e:
        print(f"❌ DELETE EVENT ERROR: {e}")
        conn.rollback()
        raise HTTPException(status_code=500, detail="שגיאה במחיקת האירוע")
    finally:
        conn.close()

@router.get("/archive")
def get_archived_events(user=Depends(require_roles(["admin", "hamal"]))):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT title, location, reporter, datetime, confirmed_by,
                       confirmed_at, arrival_time, deleted_by, deleted_at
                FROM events_archive
                ORDER BY deleted_at DESC
            """)
            rows = cursor.fetchall()
            cols = [c[0] for c in cursor.description]
            result = [dict(zip(cols, row)) for row in rows]
            print(f"📦 Archived events fetched: {len(result)} events")
            return result
    finally:
        conn.close()

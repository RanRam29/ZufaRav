# backend/routes/events_routes.py

from fastapi import APIRouter, Depends, HTTPException, Request
from db.db import get_db
from routes.auth_utils import require_roles
from routes.models.events_models import CreateEvent, JoinRequest, UpdatePeopleCount
from routes.logic.events_logic import (
    create_event_logic,
    list_events_logic,
    confirm_event_logic,
    join_event_logic,
    update_people_count_logic,
    delete_event_logic,
    get_archived_events_logic
)
from app.config.logger import logger

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/create")
def create_event(event: CreateEvent, user=Depends(require_roles(["admin", "hamal"]))):
    logger.info(f"📥 בקשת יצירת אירוע: {event.title}")
    try:
        logger.debug(f"📦 תוכן האירוע שהתקבל: {event}")
        conn = get_db()
        return create_event_logic(event, conn)
    except Exception as e:
        logger.critical(f"❌ שגיאה ב־create_event: {str(e)}")
        raise HTTPException(status_code=500, detail=f"שגיאה ב־create_event: {str(e)}")
    finally:
        try:
            conn.close()
        except:
            logger.warning("⚠️ ניסיון לסגור connection שנכשל")

@router.get("/list")
def list_events():
    logger.info("📄 טעינת כל האירועים")
    conn = get_db()
    try:
        return list_events_logic(conn)
    finally:
        conn.close()

@router.post("/confirm/{title}")
def confirm_event(title: str, request: Request, user=Depends(require_roles(["admin"]))):
    username = request.headers.get("X-User", "לא ידוע")
    logger.info(f"✅ אישור אירוע {title} ע\"י {username}")
    conn = get_db()
    try:
        return confirm_event_logic(title, username, conn)
    finally:
        conn.close()

@router.post("/join")
def join_event(data: JoinRequest, user=Depends(require_roles(["admin", "rav"]))):
    logger.info(f"➕ הצטרפות של {data.username} לאירוע {data.event_id}")
    conn = get_db()
    try:
        return join_event_logic(data.event_id, data.username, conn)
    finally:
        conn.close()

@router.patch("/update_people_count/by_id")
def update_people_count(data: UpdatePeopleCount, user=Depends(require_roles(["admin", "hamal"]))):
    logger.debug(f"🔧 עדכון כמות משתתפים לאירוע {data.id} ל-{data.new_count}")
    conn = get_db()
    try:
        return update_people_count_logic(data.id, data.new_count, conn)
    finally:
        conn.close()

@router.delete("/delete/by_id/{id}")
def delete_event(id: int, request: Request, user=Depends(require_roles(["admin"]))):
    username = request.headers.get("X-User", "לא ידוע")
    logger.warning(f"🗑️ מחיקת אירוע ID {id} על ידי {username}")
    conn = get_db()
    try:
        return delete_event_logic(id, username, conn)
    finally:
        conn.close()

@router.get("/archive")
def get_archived_events(user=Depends(require_roles(["admin", "hamal"]))):
    logger.info("📂 טעינת ארכיון האירועים")
    conn = get_db()
    try:
        return get_archived_events_logic(conn)
    finally:
        conn.close()

# backend/routes/events_routes.py

from fastapi import APIRouter, Depends, HTTPException, Request
from ZufaRav.backend.db.db import get_db
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

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/create")
def create_event(event: CreateEvent, user=Depends(require_roles(["admin", "hamal"]))):
    conn = get_db()
    return create_event_logic(event, conn)

@router.get("/list")
def list_events():
    conn = get_db()
    return list_events_logic(conn)

@router.post("/confirm/{title}")
def confirm_event(title: str, request: Request, user=Depends(require_roles(["admin"]))):
    username = request.headers.get("X-User", "לא ידוע")
    conn = get_db()
    return confirm_event_logic(title, username, conn)

@router.post("/join")
def join_event(data: JoinRequest, user=Depends(require_roles(["admin", "rav"]))):
    conn = get_db()
    return join_event_logic(data.event_id, data.username, conn)

@router.patch("/update_people_count/by_id")
def update_people_count(data: UpdatePeopleCount, user=Depends(require_roles(["admin", "hamal"]))):
    conn = get_db()
    return update_people_count_logic(data.id, data.new_count, conn)

@router.delete("/delete/by_id/{id}")
def delete_event(id: int, request: Request, user=Depends(require_roles(["admin"]))):
    username = request.headers.get("X-User", "לא ידוע")
    conn = get_db()
    return delete_event_logic(id, username, conn)

@router.get("/archive")
def get_archived_events(user=Depends(require_roles(["admin", "hamal"]))):
    conn = get_db()
    return get_archived_events_logic(conn)

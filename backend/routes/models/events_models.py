# backend/routes/models/events_models.py

from pydantic import BaseModel

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

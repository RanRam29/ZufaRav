# backend/routes/models/events_models.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime  # ✅ נדרש לשם שינוי טיפוס
from app.config.logger import logger


class CreateEvent(BaseModel):
    title: str
    location: str
    reporter: str
    severity: str = "LOW"
    people_required: int = 1
    datetime: datetime  # ✅ היה str – עכשיו datetime
    lat: float = 0.0
    lng: float = 0.0
    people_count: int = 0
    address: Optional[str] = None

    def model_post_init(self, __context):
        logger.debug(f"📥 CreateEvent INIT: {self.model_dump()}")


class JoinRequest(BaseModel):
    event_id: int
    username: str

    def model_post_init(self, __context):
        logger.debug(f"📥 JoinRequest INIT: {self.model_dump()}")


class UpdatePeopleCount(BaseModel):
    id: int
    new_count: int

    def model_post_init(self, __context):
        logger.debug(f"📥 UpdatePeopleCount INIT: {self.model_dump()}")

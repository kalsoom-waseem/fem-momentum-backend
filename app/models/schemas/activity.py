from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field as PydanticField

class ActivityCreate(BaseModel):
    user_id: int
    activity_type: str
    duration_minutes: int
    calories_burned: Optional[int] = None
    activity_date: Optional[datetime] = None
    distance_km: Optional[float] = None
    source: Optional[str] = None  # e.g. "manual", "wearable", "imported"

class ActivityRead(BaseModel):
    id: int
    user_id: int
    activity_type: str
    duration_minutes: int
    calories_burned: Optional[int] = None
    activity_date: datetime
    distance_km: Optional[float] = None
    source: Optional[str] = None
    created_at: datetime

class ActivityUpdate(BaseModel):
    activity_type: Optional[str] = None
    duration_minutes: Optional[int] = None
    calories_burned: Optional[int] = None
    activity_date: Optional[datetime] = None
    distance_km: Optional[float] = None
    source: Optional[str] = None
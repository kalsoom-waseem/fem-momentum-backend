from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field as PydanticField

class ActivityCreate(BaseModel):
    activity_type: str
    duration_minutes: int
    calories_burned: Optional[int] = None
    activity_date: Optional[datetime] = None
    distance_km: Optional[float] = None
    source: Optional[str] = None  # "manual", "wearable", "imported"


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

class ActivityRead(BaseModel):
    id: int
    user_id: int
    activity_type: str
    duration_minutes: int
    calories_burned: Optional[int]
    activity_date: datetime
    distance_km: Optional[float]
    source: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
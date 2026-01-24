from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.db.user import User


class Activity(SQLModel, table=True):
    __tablename__ = "activities_log"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(sa_column=Column(Integer, ForeignKey("user.id"), index=True))

    activity_type: str = Field(index=True)
    duration_minutes: int
    calories_burned: Optional[int] = None
    activity_date: datetime = Field(default_factory=datetime.utcnow, index=True)
    distance_km: Optional[float] = None
    source: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # ✅ forward ref
    user: "User" = Relationship(back_populates="activities")

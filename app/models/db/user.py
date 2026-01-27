from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from app.models.db.activity import Activity  # only for type hints


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(String, unique=True, index=True, nullable=False))
    hashed_password: str
    username: str | None = Field(default=None, sa_column=Column(String, unique=True, index=True))
    cycle_length_days: int = 28
    period_length_days: int = 5
    goal: str | None = None
    # ✅ use forward ref string and list built-in
    activities: list["Activity"] = Relationship(
        sa_relationship=relationship("Activity", back_populates="user")
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

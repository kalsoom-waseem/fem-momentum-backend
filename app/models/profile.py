from datetime import datetime
from sqlmodel import SQLModel, Field


class UserProfile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # basic identity (auth comes later)
    name: str | None = None

    # cycle defaults (can be edited by user later)
    cycle_length_days: int = 28
    period_length_days: int = 5

    # preferences
    goal: str | None = None  # e.g. "fat_loss", "strength", "habit"

    created_at: datetime = Field(default_factory=datetime.utcnow)

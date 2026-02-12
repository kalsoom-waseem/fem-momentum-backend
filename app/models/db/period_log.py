from __future__ import annotations

from datetime import date, datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.db.user import User


class PeriodLog(SQLModel, table=True):
    __tablename__ = "period_logs"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)

    start_date: date = Field(index=True)

    # optional overrides for this particular cycle log (v1 you can keep None)
    period_length_days: Optional[int] = None
    cycle_length_days: Optional[int] = None

    source: Optional[str] = "manual"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="period_logs")

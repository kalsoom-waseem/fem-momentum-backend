"""
User table (auth + cycle preferences).
We store hashed_password (never store plain passwords).
"""

from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy import String


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    email: str = Field(
        sa_column=Column(String, unique=True, index=True, nullable=False)
    )

    hashed_password: str = Field(nullable=False)

    cycle_length_days: int = 28
    period_length_days: int = 5
    goal: str | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

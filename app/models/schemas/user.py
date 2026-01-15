"""
Pydantic schemas for User:
- UserCreate: what client can send to signup
- UserRead: what client can see in responses
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    cycle_length_days: int = 28
    period_length_days: int = 5
    goal: str | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    cycle_length_days: int
    period_length_days: int
    goal: str | None
    created_at: datetime

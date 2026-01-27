"""
Pydantic schemas for User:
- UserCreate: what client can send to signup
- UserRead: what client can see in responses
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    username: str | None = None

    cycle_length_days: int = 28
    period_length_days: int = 5
    goal: str | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    cycle_length_days: int
    period_length_days: int
    goal: str | None
    username: str | None = None
    created_at: datetime
    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    username: Optional[str] = None
    cycle_length_days: Optional[int] = None
    period_length_days: Optional[int] = None
    goal: Optional[str] = None
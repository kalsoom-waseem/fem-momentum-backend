from datetime import date
from pydantic import BaseModel, Field


class PeriodStartCreate(BaseModel):
    start_date: date
    period_length_days: int = Field(ge=1, le=14)
    cycle_length_days: int = Field(ge=20, le=60)


class CycleDayInfo(BaseModel):
    date: date
    cycle_day: int
    phase: str
    is_period_day: bool
    is_fertile_window: bool
    is_ovulation_day: bool


class CycleRangeResponse(BaseModel):
    start: date
    end: date
    days: list[CycleDayInfo]

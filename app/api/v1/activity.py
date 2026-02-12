from __future__ import annotations

from datetime import date, datetime, time
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Query
from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser
from app.models.db.activity import Activity
from app.models.schemas.activity import ActivityCreate, ActivityRead, ActivityUpdate

router = APIRouter()

def _to_dt_start(d: date) -> datetime:
    return datetime.combine(d, time.min)


def _to_dt_end(d: date) -> datetime:
    return datetime.combine(d, time.max)


@router.post("", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
def create_activity(payload: ActivityCreate, session: SessionDep, current_user: CurrentUser):
    activity = Activity(
        user_id=current_user.id,
        activity_type=payload.activity_type,
        duration_minutes=payload.duration_minutes,
        calories_burned=payload.calories_burned,
        distance_km=payload.distance_km,
        source=payload.source,
        activity_date=payload.activity_date or datetime.utcnow(),
    )
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity


@router.get("", response_model=List[ActivityRead])
def list_activities(
    session: SessionDep,
    current_user: CurrentUser,
    activity_type: Optional[str] = Query(default=None, description="Filter by activity_type (exact match)"),
    source: Optional[str] = Query(default=None, description="Filter by source (e.g. manual/wearable/imported)"),
    date_from: Optional[date] = Query(default=None, description="Start date (inclusive), e.g. 2026-01-01"),
    date_to: Optional[date] = Query(default=None, description="End date (inclusive), e.g. 2026-01-31"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    sort: str = Query(default="-activity_date", description="activity_date or -activity_date"),
):
    stmt = select(Activity).where(Activity.user_id == current_user.id)

    if activity_type:
        stmt = stmt.where(Activity.activity_type == activity_type)

    if source:
        stmt = stmt.where(Activity.source == source)

    if date_from:
        stmt = stmt.where(Activity.activity_date >= _to_dt_start(date_from))

    if date_to:
        stmt = stmt.where(Activity.activity_date <= _to_dt_end(date_to))

    if sort == "activity_date":
        stmt = stmt.order_by(Activity.activity_date.asc())
    else:
        # default newest first
        stmt = stmt.order_by(Activity.activity_date.desc())

    stmt = stmt.offset(offset).limit(limit)

    return session.exec(stmt).all()


@router.get("/{activity_id}", response_model=ActivityRead)
def get_activity(activity_id: int, session: SessionDep, current_user: CurrentUser):
    stmt = select(Activity).where(
        Activity.id == activity_id,
        Activity.user_id == current_user.id,  # ✅ user can only access their own record
    )
    activity = session.exec(stmt).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.patch("/{activity_id}", response_model=ActivityRead)
def update_activity(
    activity_id: int,
    payload: ActivityUpdate,
    session: SessionDep,
    current_user: CurrentUser,
):
    stmt = select(Activity).where(
        Activity.id == activity_id,
        Activity.user_id == current_user.id,  # ✅ ownership check
    )
    activity = session.exec(stmt).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    data = payload.model_dump(exclude_unset=True)

    # ✅ Never allow changing ownership, even if someone tries
    data.pop("user_id", None)

    for k, v in data.items():
        setattr(activity, k, v)

    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity

@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(activity_id: int, session: SessionDep, current_user: CurrentUser):
    stmt = select(Activity).where(
        Activity.id == activity_id,
        Activity.user_id == current_user.id,  # ✅ ownership check
    )
    activity = session.exec(stmt).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    session.delete(activity)
    session.commit()
    return None


from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser
from app.models.db.activity import Activity
from app.models.schemas.activity import ActivityCreate, ActivityRead, ActivityUpdate

router = APIRouter()

@router.post("/", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
def create_activity(payload: ActivityCreate, session: SessionDep, user:CurrentUser):
    """Create a new activity log entry."""
    activity = Activity(
        user_id=payload.user_id,
        activity_type=payload.activity_type,
        duration_minutes=payload.duration_minutes,
        calories_burned=payload.calories_burned,
        activity_date=payload.activity_date or datetime.utcnow(),
        distance_km=payload.distance_km,
        source=payload.source
    )
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity


@router.get("/", response_model=list[ActivityRead])
def list_activities(session: SessionDep, user: CurrentUser, limit: int = 50, offset: int = 0):
    stmt = (
        select(Activity)
        .where(Activity.user_id == user.id)
        .order_by(Activity.activity_date.desc())
        .offset(offset)
        .limit(limit)
    )
    return session.exec(stmt).all()


@router.patch("/{activity_id}", response_model=ActivityRead)
def update_activity(activity_id: int, payload: ActivityUpdate, session: SessionDep, user: CurrentUser):
    activity = session.get(Activity, activity_id)
    if not activity or activity.user_id != user.id:
        raise HTTPException(status_code=404, detail="Activity not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(activity, key, value)

    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(activity_id: int, session: SessionDep, user: CurrentUser):
    activity = session.get(Activity, activity_id)
    if not activity or activity.user_id != user.id:
        raise HTTPException(status_code=404, detail="Activity not found")

    session.delete(activity)
    session.commit()
    return
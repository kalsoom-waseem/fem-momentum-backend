from datetime import date, timedelta

from fastapi import APIRouter, HTTPException

from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser
from app.models.db.period_log import PeriodLog
from app.models.schemas.cycle import PeriodStartCreate, CycleRangeResponse, CycleDayInfo
from app.services.cycle_engine import day_info

router = APIRouter(prefix="/cycle", tags=["cycle"])


def get_anchor_log(session: SessionDep, user_id: int)->PeriodLog:
    log = session.exec(select(PeriodLog).where(PeriodLog.user_id == user_id).order_by(PeriodLog.start_date.desc())).first()

    if not log:
        raise HTTPException(status_code=400, detail="No period start found. Please add period date first.")
    return log


@router.post("/period-start")
def add_period_start(payload:PeriodStartCreate, session: SessionDep, current_user: CurrentUser):
    log= PeriodLog(
        user_id = current_user.id,
        start_date = payload.start_date,
        period_length_days= payload.period_length_days,
        cycle_length_days= payload.cycle_length_days,
        source="manual"
    )
    session.add(log)
    current_user.period_length_days = payload.period_length_days
    current_user.cycle_length_days = payload.cycle_length_days
    session.add(current_user)

    session.commit()
    session.refresh(log)

    return {"message": "Period start saved", "period_log_id": log.id}

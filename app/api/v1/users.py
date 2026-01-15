from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep, CurrentUser
from app.models.user import User
from app.models.schemas.user import UserRead

router = APIRouter()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: SessionDep, current_user: CurrentUser):
    # simple protection: allow reading only yourself
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

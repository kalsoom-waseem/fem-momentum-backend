from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep, CurrentUser
from app.models.db.user import User
from app.models.schemas.user import UserRead, UserUpdate

router = APIRouter()

@router.get("/me", response_model= UserRead)
def read_me(current_user: CurrentUser):
    return current_user

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: SessionDep, current_user: CurrentUser):
    # simple protection: allow reading only yourself
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/me", response_model=UserRead)
def update_me(payload: UserUpdate, session: SessionDep, current_user: CurrentUser):
    data = payload.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(current_user, key, value)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user
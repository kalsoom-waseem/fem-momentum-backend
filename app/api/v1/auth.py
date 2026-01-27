from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.api.deps import SessionDep, CurrentUser
from app.core.database import get_session
from app.core.security import hash_password, verify_password, create_access_token
from app.models.db.user import User
from app.models.schemas.user import UserCreate, UserRead
from app.models.schemas.auth import LoginRequest, Token

router = APIRouter()


@router.post("/signup", response_model=UserRead)
def signup(payload: UserCreate, session: SessionDep):
    existing = session.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        cycle_length_days=payload.cycle_length_days,
        period_length_days=payload.period_length_days,
        goal=payload.goal,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session),):
    # form_data.username will contain what you type in Swagger "username"
    user = session.exec(select(User).where(User.email == form_data.username)).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(user.email)
  # or subject=user.email
    return {"access_token": access_token, "token_type": "bearer"}
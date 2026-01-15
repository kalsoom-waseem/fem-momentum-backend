from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
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


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, session: SessionDep):
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(subject=user.email)
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
def me(current_user: CurrentUser):
    return current_user

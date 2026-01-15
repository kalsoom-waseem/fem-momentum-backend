from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.models.profile import UserProfile

router = APIRouter()

@router.post("/")
def create_profile(profile: UserProfile, session: SessionDep):
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile

@router.get("/{profile_id}")
def get_profile(profile_id: int, session: SessionDep):
    profile = session.get(UserProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

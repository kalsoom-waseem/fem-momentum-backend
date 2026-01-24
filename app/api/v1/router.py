from fastapi import APIRouter
from app.api.v1 import auth, users, activity

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(activity.router, prefix="/activities", tags=["activities"])

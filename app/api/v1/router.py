from fastapi import APIRouter
from app.api.v1 import profiles

router = APIRouter()
router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])

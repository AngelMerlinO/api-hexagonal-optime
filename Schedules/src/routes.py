from fastapi import APIRouter
from src.schedules.infraestructure.scheduleRouter import router as schedule_router

router = APIRouter()

router.include_router(schedule_router)
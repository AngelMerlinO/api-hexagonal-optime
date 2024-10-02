# src/routes.py
from fastapi import APIRouter
from src.users.infrastructure.UserRoutes import router as user_router
from src.schedules.infrastructure.ScheduleRoutes import router as schedule_router

router = APIRouter()

# Incluir todas las rutas de las diferentes entidades
router.include_router(user_router)
router.include_router(schedule_router)
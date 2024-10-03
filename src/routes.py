# src/routes.py
from fastapi import APIRouter
from src.users.infrastructure.UserRoutes import router as user_router
from src.schedules.infrastructure.ScheduleRoutes import router as schedule_router
from src.notifications.infrastructure.NotificationRoutes import router as notification_router
from src.Activities.infraestructure.ActivitiesRouter import router as activities_router

router = APIRouter()

# Incluir todas las rutas de las diferentes entidades
router.include_router(user_router)
router.include_router(schedule_router)
router.include_router(notification_router)
router.include_router(activities_router)

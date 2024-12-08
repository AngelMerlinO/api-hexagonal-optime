from fastapi import APIRouter
from src.notifications.infrastructure.NotificationRoutes import router as notification_router

router = APIRouter()

router.include_router(notification_router)


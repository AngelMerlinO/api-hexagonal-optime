from fastapi import APIRouter
from src.users.infrastructure.UserRoutes import router as user_router
from src.schedules.infrastructure.ScheduleRoutes import router as schedule_router
from src.notifications.infrastructure.NotificationRoutes import router as notification_router
from src.Activities.infraestructure.ActivitiesRouter import router as activities_router
from src.payments.infrastructure.PaymentRoutes import router as payment_router
from src.messaging.infrastructure.MessageRoutes import router as messaging_router
from src.contact.infraestructure.ContactRouter import router as contact_router

router = APIRouter()

router.include_router(user_router)
router.include_router(schedule_router)
router.include_router(notification_router)
router.include_router(activities_router)
router.include_router(payment_router)
router.include_router(messaging_router)
router.include_router(contact_router)


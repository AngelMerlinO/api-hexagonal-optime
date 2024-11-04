from fastapi import APIRouter
from src.users.infrastructure.UserRoutes import router as user_router
from src.contact.infraestructure.ContactRouter import router as contact_router

router = APIRouter()

router.include_router(user_router)

router.include_router(contact_router)


from fastapi import APIRouter
from src.users.infrastructure.UserRoutes import router as user_router

router = APIRouter()

# Incluir todas las rutas de las diferentes entidades
router.include_router(user_router)

from fastapi import APIRouter
from src.payments.infrastructure.PaymentRoutes import router as payment_router

router = APIRouter()

router.include_router(payment_router)


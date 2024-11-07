from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.payments.infrastructure.MySqlPaymentRepository import MySqlPaymentRepository
from src.payments.infrastructure.MercadoPagoService import MercadoPagoService
from src.payments.infrastructure.PaymentDependecies import get_payment_service
from config.database import get_db
from pydantic import BaseModel
from typing import List, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/api/v1/payments",
    tags=["payments"]
)

class PaymentItemModel(BaseModel):
    title: str
    quantity: int
    unit_price: float
    currency_id: str = 'MXN'

class PayerModel(BaseModel):
    email: str

class PaymentCreateModel(BaseModel):
    user_id: int
    items: List[PaymentItemModel]
    payer: PayerModel
    description: Optional[str] = None

@router.post("/")
@limiter.limit("5/minute")
async def create_payment(
    request: Request,
    payment_data: PaymentCreateModel,
    payment_service = Depends(get_payment_service)
):
    try:
        result = payment_service.create_payment(
            user_id=payment_data.user_id,
            items=[item.dict() for item in payment_data.items],
            payer=payment_data.payer.dict(),
            description=payment_data.description
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/notifications")
@limiter.limit("5/minute")
async def receive_notifications(
    request: Request,
    payment_service = Depends(get_payment_service)
):
    try:
        data = await request.json()
        ##print(f"Notification data received: {data}")

        payment = payment_service.process_notification(data)
        return {"status": payment.status, "message_id": payment.payment_id}
    except Exception as e:
        print(f"Error processing notification: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/retorno")
@limiter.limit("5/minute")
async def payment_return(
    request: Request,
    payment_service = Depends(get_payment_service)
):
    query_params = request.query_params
    payment_id = query_params.get("payment_id") or query_params.get("collection_id")
    status_param = query_params.get("status")

    try:
        if payment_id:
            payment = payment_service.get_payment_status(payment_id)
            return {
                "message": f"Tu pago ha sido {payment.status}.",
                "payment_id": payment.payment_id,
                "status": payment.status,
                "status_detail": payment.status_detail
            }
        else:
            return {
                "message": "No se pudo obtener información del pago.",
                "status": status_param
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
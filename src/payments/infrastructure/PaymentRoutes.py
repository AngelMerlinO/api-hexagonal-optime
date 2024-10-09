from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.payments.application.PaymentProcessor import PaymentProcessor
from src.payments.infrastructure.MySqlPaymentRepository import MySqlPaymentRepository
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from config.database import get_db
from pydantic import BaseModel
from typing import List, Optional

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
async def create_payment(
    payment_data: PaymentCreateModel,
    db: Session = Depends(get_db)
):
    payment_repo = MySqlPaymentRepository(db)
    user_repo = MySqlUserRepository(db)
    payment_processor = PaymentProcessor(payment_repo, user_repo)

    try:
        result = payment_processor.create_payment(
            payment_data.user_id,
            [item.dict() for item in payment_data.items],
            payment_data.payer.dict(),
            payment_data.description
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/notifications")
async def receive_notifications(request: Request, db: Session = Depends(get_db)):
    payment_repo = MySqlPaymentRepository(db)
    user_repo = MySqlUserRepository(db)
    payment_processor = PaymentProcessor(payment_repo, user_repo)

    try:
        data = await request.json()
        print("Notification data received:", data)  # Para depuración

        # Procesa la notificación
        payment = payment_processor.process_notification(data)
        print(f"Payment {payment.payment_id} updated")

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/retorno")
async def payment_return(request: Request, db: Session = Depends(get_db)):
    query_params = request.query_params
    status_param = query_params.get("status")
    payment_id = query_params.get("payment_id") or query_params.get("collection_id")
    preference_id = query_params.get("preference_id")

    payment_repo = MySqlPaymentRepository(db)
    user_repo = MySqlUserRepository(db)
    payment_processor = PaymentProcessor(payment_repo, user_repo)

    if payment_id:
        try:
            payment = payment_processor.get_payment_status(payment_id)
            return {
                "message": f"Tu pago ha sido {payment.status}.",
                "payment_id": payment.payment_id,
                "status": payment.status,
                "status_detail": payment.status_detail
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        return {
            "message": "No se pudo obtener información del pago.",
            "status": status_param
        }
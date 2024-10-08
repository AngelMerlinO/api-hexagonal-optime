from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session
from src.payments.application.PaymentProcessor import PaymentProcessor
from src.payments.infrastructure.MySqlPaymentRepository import MySqlPaymentRepository
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from config.database import get_db, SessionLocal  
from pydantic import BaseModel
from typing import List, Optional
from src.users.domain.exceptions import UserNotFoundException
from src.payments.domain.exceptions import PaymentProcessingException, PaymentNotFoundException

router = APIRouter(
    prefix=("/api/v1/payments")
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
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PaymentProcessingException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/notifications")
async def receive_notifications(request: Request):
    db = SessionLocal()
    try:
        try:
            data = await request.json()
        except:
            data = dict(request.query_params)

        print("Datos de la notificación recibidos:", data)

        payment_repo = MySqlPaymentRepository(db)
        user_repo = MySqlUserRepository(db)
        payment_processor = PaymentProcessor(payment_repo, user_repo)
        payment = payment_processor.process_notification(data)
        print(f"Notificación procesada. Pago actualizado: {payment}")

        return {"status": "success"}
    except Exception as e:
        print("Error procesando la notificación:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()
        print("Sesión de base de datos cerrada")


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
            status = payment.status
            status_detail = payment.status_detail

            if status == "approved":
                mensaje = "Tu pago ha sido aprobado."
            elif status == "rejected":
                mensaje = "Tu pago ha sido rechazado."
            elif status == "in_process":
                mensaje = "Tu pago está en proceso."
            else:
                mensaje = f"Estado de tu pago: {status}"

            return {
                "message": mensaje,
                "payment_id": payment_id,
                "status": status,
                "status_detail": status_detail
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        return {
            "message": "No se pudo obtener información del pago.",
            "status": status_param
        }

@router.get("/status/{payment_id}")
async def get_payment_status(payment_id: str, db: Session = Depends(get_db)):
    payment_repo = MySqlPaymentRepository(db)
    user_repo = MySqlUserRepository(db)
    payment_processor = PaymentProcessor(payment_repo, user_repo)
    try:
        payment = payment_processor.get_payment_status(payment_id)
        return {
            "payment_id": payment.payment_id,
            "status": payment.status,
            "status_detail": payment.status_detail
        }
    except PaymentNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
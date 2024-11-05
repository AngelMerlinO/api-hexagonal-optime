from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.payments.application.PaymentProcessor import PaymentProcessor
from src.payments.infrastructure.MySqlPaymentRepository import MySqlPaymentRepository
from src.payments.infrastructure.MercadoPagoService import MercadoPagoService
from src.payments.infrastructure.RabbitMQPaymentPublisher import RabbitMQPaymentPublisher
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
    mercado_pago_service = MercadoPagoService()
    publisher = RabbitMQPaymentPublisher(host='34.236.102.207', username='usuario', password='password')
    payment_processor = PaymentProcessor(payment_repo, mercado_pago_service, publisher)

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
    finally:
        publisher.close()  # Cerrar la conexión a RabbitMQ

@router.post("/notifications")
async def receive_notifications(request: Request, db: Session = Depends(get_db)):
    payment_repo = MySqlPaymentRepository(db)
    mercado_pago_service = MercadoPagoService()
    publisher = RabbitMQPaymentPublisher(host='34.236.102.207', username='usuario', password='password')
    payment_processor = PaymentProcessor(payment_repo, mercado_pago_service, publisher)

    try:
        # Obtener la notificación de Mercado Pago
        data = await request.json()
        print(f"Notification data received: {data}")

        # Procesar la notificación de pago
        payment = payment_processor.process_notification(data)
        
        # Información del destinatario y contenido del mensaje
        recipient_phone_number = "529515271070" 
        status = payment.status
        amount = f"{payment.amount}"
        currency = payment.currency_id
        payment_id = payment.payment_id

        # Publicar en la cola si el pago ha sido aprobado
        if payment.status == "approved":
            event = {
                "payment_id": payment.payment_id,
                "user_id": payment.user_id,
                "amount": payment.amount,
                "currency_id": payment.currency_id,
                "status": payment.status,
                "date_created": payment.date_created.isoformat() if payment.date_created else None
            }
            publisher.publish(event)

        return {"status": "-", "message_id": payment.payment_id}
    except Exception as e:
        print(f"Error processing notification: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        publisher.close()  # Cerrar la conexión a RabbitMQ

@router.get("/retorno")
async def payment_return(request: Request, db: Session = Depends(get_db)):
    query_params = request.query_params
    status_param = query_params.get("status")
    payment_id = query_params.get("payment_id") or query_params.get("collection_id")
    preference_id = query_params.get("preference_id")

    payment_repo = MySqlPaymentRepository(db)
    mercado_pago_service = MercadoPagoService()
    publisher = RabbitMQPaymentPublisher(host='34.236.102.207', username='usuario', password='password')
    payment_processor = PaymentProcessor(payment_repo, mercado_pago_service, publisher)

    if payment_id:
        try:
            # Obtener el estado del pago
            payment = payment_processor.get_payment_status(payment_id)

            # Publicar en la cola si el pago ha sido aprobado
            if payment.status == "approved":
                event = {
                    "payment_id": payment.payment_id,
                    "user_id": payment.user_id,
                    "amount": payment.amount,
                    "currency_id": payment.currency_id,
                    "status": payment.status,
                    "date_created": payment.date_created.isoformat() if payment.date_created else None
                }
                publisher.publish(event)

            # Devolver la respuesta al cliente
            return {
                "message": f"Tu pago ha sido {payment.status}.",
                "payment_id": payment.payment_id,
                "status": payment.status,
                "status_detail": payment.status_detail
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            publisher.close()  # Asegurarse de cerrar la conexión
    else:
        return {
            "message": "No se pudo obtener información del pago.",
            "status": status_param
        }
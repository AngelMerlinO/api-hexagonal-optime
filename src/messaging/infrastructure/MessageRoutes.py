from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from src.messaging.application.MessageSender import MessageSender
from src.messaging.infrastructure.MySqlMessageRepository import MySqlMessageRepository
from src.messaging.infrastructure.WhatsAppService import WhatsAppService  # Importamos el servicio
from config.database import get_db
from slowapi.util import get_remote_address
from slowapi import Limiter
from src.messaging.domain.exceptions import MessageSendingException
from datetime import datetime

limiter= Limiter(key_func=get_remote_address)

router = APIRouter()

class PaymentConfirmationModel(BaseModel):
    recipient_phone_number: str = Field(..., example="529515271070")
    status: str = Field(..., example="aprobado")
    amount: str = Field(..., example="1000")
    currency: str = Field(..., example="MXN")
    payment_id: str = Field(..., example="12345")

class MessageResponseModel(BaseModel):
    id: int
    recipient_phone_number: str
    message_type: str
    message_content: str
    status: str
    updated_at: datetime

    class Config:
        from_attributes = True  # Habilitar para que funcione con ORMs

@router.post("/api/v1/send-payment-confirmation", response_model=MessageResponseModel)
@limiter.limit("2/minute")  
def send_payment_confirmation(message_data: PaymentConfirmationModel,request:Request, db: Session = Depends(get_db)):
    message_repo = MySqlMessageRepository(db)
    whatsapp_service = WhatsAppService()  # Crear instancia del servicio
    message_sender = MessageSender(message_repo, whatsapp_service)

    try:
        # Enviar la confirmación de pago
        saved_message = message_sender.send_payment_confirmation(
            recipient_phone_number=message_data.recipient_phone_number,
            status=message_data.status,
            amount=message_data.amount,
            currency=message_data.currency,
            payment_id=message_data.payment_id
        )

        # Obtener el mensaje desde la base de datos y devolverlo
        message_from_db = message_repo.find_by_id(saved_message.id)
        return message_from_db

    except MessageSendingException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
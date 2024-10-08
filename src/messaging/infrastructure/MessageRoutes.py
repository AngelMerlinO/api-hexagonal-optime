from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from src.messaging.application.MessageSender import MessageSender
from src.messaging.infrastructure.MySqlMessageRepository import MySqlMessageRepository
from config.database import get_db
from src.messaging.domain.exceptions import MessageSendingException
from datetime import datetime  # Importar datetime

router = APIRouter()


class MessageCreateModel(BaseModel):
    recipient_phone_number: str = Field(..., example="529515271070")
    message_type: str = Field(..., example="template")  # e.g., "template", "text"
    message_content: str = Field(..., example="hello_world")  # Nombre de la plantilla o contenido del mensaje

class MessageResponseModel(BaseModel):
    id: int
    recipient_phone_number: str
    message_type: str
    message_content: str
    status: str
    error_message: Optional[str] = None
    date_created: datetime  # Cambiar de str a datetime
    updated_at: datetime    # Cambiar de str a datetime

    class Config:
        orm_mode = True  # Habilitar orm_mode


@router.post("/api/v1/send-message", response_model=MessageResponseModel)
def send_message(message_data: MessageCreateModel, db: Session = Depends(get_db)):
    message_repo = MySqlMessageRepository(db)
    message_sender = MessageSender(message_repo)

    try:
        message = message_sender.send_whatsapp_message(
            recipient_phone_number=message_data.recipient_phone_number,
            message_type=message_data.message_type,
            message_content=message_data.message_content
        )
        return message
    except MessageSendingException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


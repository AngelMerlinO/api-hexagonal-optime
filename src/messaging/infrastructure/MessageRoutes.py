from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from src.messaging.application.MessageSender import MessageSender
from src.messaging.infrastructure.MySqlMessageRepository import MySqlMessageRepository
from config.database import get_db
from src.messaging.domain.exceptions import MessageSendingException
from datetime import datetime


router = APIRouter()

class MessageCreateModel(BaseModel):
    recipient_phone_number: str = Field(..., example="529515271070")
    message_content: str = Field(..., example="hello_world")

class MessageResponseModel(BaseModel):
    id: int
    recipient_phone_number: str
    message_type: str
    message_content: str
    status: str
    updated_at: datetime  # Este campo es obligatorio en la respuesta

    class Config:
        orm_mode = True  # Asegúrate de que el orm_mode esté activado en V2, usa 'from_attributes' en lugar de 'orm_mode'

@router.post("/api/v1/send-message", response_model=MessageResponseModel)
def send_message(message_data: MessageCreateModel, db: Session = Depends(get_db)):
    print("Conectando a la base de datos...")
    message_repo = MySqlMessageRepository(db)
    message_sender = MessageSender(message_repo)

    try:
        print("Enviando mensaje a:", message_data.recipient_phone_number)

        # Send the message and save it to the database
        saved_message = message_sender.send_whatsapp_message(
            recipient_phone_number=message_data.recipient_phone_number,
            message_content=message_data.message_content
        )

        print("Mensaje enviado correctamente")

        # Retrieve the message using the id from the saved message
        message_from_db = message_repo.find_by_id(saved_message.id)
        return message_from_db

    except MessageSendingException as e:
        print("Error al enviar mensaje:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
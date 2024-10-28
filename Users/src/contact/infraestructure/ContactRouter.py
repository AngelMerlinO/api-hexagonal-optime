from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.contact.application.ContactCreator import ContactCreator
from src.contact.infraestructure.MySqlContactRepository import MySqlContactRepository
from src.contact.infraestructure.HttpContactNotificationService import HttpContactNotificationService
from slowapi.util import get_remote_address
from slowapi import Limiter
from config.database import get_db
from pydantic import BaseModel

from src.contact.domain.exceptions import ContactAlreadyExistsException, InvalidContactDataException
import os
from dotenv import load_dotenv


limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/api/v1/contacts",
    tags=["contacts"]
)

class ContactCreate(BaseModel):
    email: str
    phone: str


LAMBDA_URL = os.getenv("AWS_ACCESS_CREATE_OPT")

@router.post("/")
@limiter.limit("2/minute")  
def create_contact(contact_data: ContactCreate, request:Request, db: Session = Depends(get_db)):
    contact_repo = MySqlContactRepository(db)
    notification_service = HttpContactNotificationService(lambda_url=LAMBDA_URL)  # Inyectar el servicio de notificación
    
    contact_creator = ContactCreator(contact_repo, notification_service)
    
    try:
        contact_model = contact_creator.create(
            email=contact_data.email, 
            phone=contact_data.phone
        )
        
        return {"message": "Contact created successfully", "contact_id": contact_model.id}
    
    except ContactAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    
    except InvalidContactDataException as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
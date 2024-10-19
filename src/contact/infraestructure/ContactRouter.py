from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.contact.application.ContactCreator import ContactCreator
from src.contact.application.ContactFindById import ContactFindByID
from src.contact.infraestructure.MySqlContactRepository import MySqlContactRepository
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from config.database import get_db
from pydantic import BaseModel
from fastapi import Query

from src.contact.domain.exceptions import ContactAlreadyExistsException, InvalidContactDataException

router = APIRouter(
    prefix="/api/v1/contacts",
    tags=["contacts"]
)

class ContactCreate(BaseModel):
    email: str
    phone: str

class ContactUpdate(BaseModel):
    email: str = None
    phone: str = None

@router.get("/{contact_id}")
def find_contact_by_id(contact_id: int, db: Session = Depends(get_db)):
    contact_repo = MySqlContactRepository(db)
    contact_finder = ContactFindByID(contact_repo)
    
    try:
        contact = contact_finder.find_by_id(contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail=f"Contact with ID {contact_id} not found")
        
        return {
            "id": contact.id,
            "email": contact.email,
            "phone": contact.phone,
            "created_at": contact.created_at,
            "updated_at": contact.updated_at,
            "deleted_at": contact.deleted_at
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error finding contact: {str(e)}")

@router.post("/")
def create_contact(contact_data: ContactCreate, db: Session = Depends(get_db)):
    contact_repo = MySqlContactRepository(db)
    
    contact_creator = ContactCreator(contact_repo)
    
    try:
        contact_model = contact_creator.create(
            email=contact_data.email, 
            phone=contact_data.phone
        )
        
        db.commit()
        db.refresh(contact_model)

        return {"message": "Contact created successfully", "contact_id": contact_model.id}
    
    except ContactAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    
    except InvalidContactDataException as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




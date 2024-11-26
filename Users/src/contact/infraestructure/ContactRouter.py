from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi.util import get_remote_address
from slowapi import Limiter
from pydantic import BaseModel
from src.contact.domain.exceptions import ContactAlreadyExistsException, InvalidContactDataException
from src.contact.infraestructure.ContactDependencies import get_contact_service
from src.contact.application.services.ContactService import ContactService

# Configuración del limitador de tasa de solicitudes
limiter = Limiter(key_func=get_remote_address)

# Definir el enrutador de contactos
router = APIRouter(
    prefix="/api/v1/contacts",
    tags=["contacts"]
)

# Modelo para los datos de creación de contacto
class ContactCreate(BaseModel):
    email: str
    phone: str
    name: str
    last_name: str

# Ruta para crear un contacto
@router.post("/")
@limiter.limit("2/minute")
def create_contact(contact_data: ContactCreate, request: Request, contact_service=Depends(get_contact_service)):
    try:
        # Llamar al servicio de contacto para crear el contacto
        new_contact = contact_service.create_contact(
            email=contact_data.email,
            phone=contact_data.phone,
            name=contact_data.name,
            last_name=contact_data.last_name
        )
        
        # Retornar el ID del contacto creado
        return {"message": "Contact created successfully", "contact_id": new_contact.id}
    
    except ContactAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    
    except InvalidContactDataException as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
        raise HTTPException(status_code=500, detail="Internal Server Error")

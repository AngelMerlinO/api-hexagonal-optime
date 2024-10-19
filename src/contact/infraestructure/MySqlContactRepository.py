from typing import List, Optional
from sqlalchemy.orm import Session
from src.contact.domain.ContactRepository import ContactRepository
from src.contact.domain.Contact import Contact
from src.contact.infraestructure.orm.ContactModel import ContactModel

class MySqlContactRepository(ContactRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def save(self, contact: ContactModel) -> ContactModel:
        """Guarda o actualiza un contacto en la base de datos."""
        self.db_session.add(contact)
        self.db_session.commit()
        self.db_session.refresh(contact)
        return contact
    
    def find_by_email_or_phone(self, email: str, phone: str) -> Optional[ContactModel]:
        """Busca un contacto por email o teléfono."""
        return self.db_session.query(ContactModel).filter(
            (ContactModel.email == email) | (ContactModel.phone == phone)
        ).first()
    
    def update_by_id(self, contact_id: int, email: Optional[str], phone: Optional[str]) -> None:
        """Actualiza un contacto en la base de datos por su ID."""
        contact_model = self.db_session.query(ContactModel).filter_by(id=contact_id).first()
        if not contact_model:
            raise ValueError(f"Contact with ID {contact_id} not found")

        if email:
            contact_model.email = email
        if phone:
            contact_model.phone = phone
        self.db_session.commit()
    
    def find_by_id(self, contact_id: int) -> Optional[ContactModel]:
        """Busca un contacto por su ID (debería devolver un ContactModel, no Contact)."""
        return self.db_session.query(ContactModel).filter_by(id=contact_id).first()
    
    def get_by_id(self, contact_id: int) -> ContactModel:
        return self.find_by_id(contact_id)
    
    def find_all(self) -> List[Contact]:
        """Devuelve todos los contactos no eliminados (soft delete)."""
        contacts_models = self.db_session.query(ContactModel).filter_by(deleted_at=None).all()
        
        return [
            Contact(
                id=contact_model.id,
                email=contact_model.email,
                phone=contact_model.phone,
                created_at=contact_model.created_at,
                updated_at=contact_model.updated_at,
                deleted_at=contact_model.deleted_at
            )
            for contact_model in contacts_models
        ]
    
    def delete_by_id(self, contact_id: int) -> None:
        """Elimina un contacto por su ID."""
        contact_model = self.db_session.query(ContactModel).filter_by(id=contact_id).first()
        if not contact_model:
            raise ValueError(f"Contact with ID {contact_id} not found")

        self.db_session.delete(contact_model)
        self.db_session.commit()

from typing import List, Optional
from sqlalchemy.orm import Session
from src.contact.domain.ContactRepository import ContactRepository
from src.contact.domain.Contact import Contact
from src.contact.infraestructure.orm.ContactModel import ContactModel

class MySqlContactRepository(ContactRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def save(self, contact: Contact) -> Contact:
        contact_model = ContactModel(
            email=contact.email,
            phone=contact.phone,
            name=contact.name,
            last_name=contact.last_name,
        )

        # Agrega y realiza un flush para obtener el ID sin cerrar la transacción
        self.db_session.add(contact_model)
        self.db_session.flush()
        self.db_session.refresh(contact_model)  # Refresca para obtener el ID

        print(f"ID después de flush y refresh: {contact_model.id}")  # Verifica que el ID esté presente

        return Contact(
            id=contact_model.id,
            email=contact_model.email,
            phone=contact_model.phone,
            name=contact_model.name,
            last_name=contact_model.last_name,
            created_at=contact_model.created_at,
            updated_at=contact_model.updated_at,
            deleted_at=contact_model.deleted_at
        )
    
    def find_by_email_or_phone(self, email: str, phone: str, name: str, last_name: str) -> Optional[ContactModel]:
        """Busca un contacto por email o teléfono."""
        return self.db_session.query(ContactModel).filter(
            (ContactModel.email == email) | (ContactModel.phone == phone) | (ContactModel.name == name) | (ContactModel.last_name == last_name)
        ).first()
    
    def update_by_id(self, contact_id: int, email: Optional[str], phone: Optional[str], name: Optional[str], last_name: Optional[str]):
        """Actualiza un contacto en la base de datos por su ID."""
        contact_model = self.db_session.query(ContactModel).filter_by(id=contact_id).first()
        if not contact_model:
            raise ValueError(f"Contact with ID {contact_id} not found")

        if email:
            contact_model.email = email
        if phone:
            contact_model.phone = phone
        if name:
            contact_model.name = name
        if last_name:
            contact_model.last_name = last_name
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
                name=contact_model.name,
                last_name=contact_model.last_name,
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

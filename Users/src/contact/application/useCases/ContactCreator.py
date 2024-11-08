from src.contact.domain.ContactRepository import ContactRepository
from src.contact.domain.exceptions import ContactAlreadyExistsException, InvalidContactDataException
from src.contact.infraestructure.orm.ContactModel import ContactModel
from src.contact.domain.Contact import Contact

class ContactCreator:
    def __init__(self, contact_repository: ContactRepository):
        self.contact_repository = contact_repository

    def create(
        self,
        email: str,
        phone: str,
        name: str,
        last_name: str
    ) -> Contact:
        existing_contact = self.contact_repository.find_by_email_or_phone(email, phone, name, last_name)
        if existing_contact:
            raise ContactAlreadyExistsException(f"Contact with email '{email}' or phone '{phone}' already exists")

        if not self._validate_email(email):
            raise InvalidContactDataException(f"Invalid email format: {email}")
        if not self._validate_phone(phone):
            raise InvalidContactDataException(f"Invalid phone format: {phone}")

        # Crea y guarda el modelo ContactModel
        new_contact_model = ContactModel(
            email=email,
            phone=phone,
            name=name,
            last_name=last_name
        )

        # Guarda y asegura que el id esté disponible
        saved_contact_model = self.contact_repository.save(new_contact_model)

        # Convierte el ContactModel guardado en un Contact y lo devuelve
        return Contact(
            id=saved_contact_model.id,
            email=saved_contact_model.email,
            phone=saved_contact_model.phone,
            name=saved_contact_model.name,
            last_name=saved_contact_model.last_name,
            created_at=saved_contact_model.created_at,
            updated_at=saved_contact_model.updated_at,
            deleted_at=saved_contact_model.deleted_at
        )

    def _validate_email(self, email: str) -> bool:
        return '@' in email and '.' in email

    def _validate_phone(self, phone: str) -> bool:
        return phone.isdigit() and len(phone) <= 20
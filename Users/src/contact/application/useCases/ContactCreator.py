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

        new_contact_model = ContactModel(
            email=email,
            phone=phone,
            name=name,
            last_name=last_name
        )

        self.contact_repository.save(new_contact_model)

        return new_contact_model

    def _validate_email(self, email: str) -> bool:
        """Validar si el formato de email es válido."""
        return '@' in email and '.' in email

    def _validate_phone(self, phone: str) -> bool:
        """Validar si el formato del teléfono es válido (longitud o caracteres permitidos)."""
        return phone.isdigit() and len(phone) <= 20
from src.contact.domain.ContactRepository import ContactRepository
from src.contact.domain.ContactNotificationService import ContactNotificationService
from src.contact.domain.exceptions import ContactAlreadyExistsException, InvalidContactDataException
from src.contact.infraestructure.orm.ContactModel import ContactModel

class ContactCreator:
    def __init__(self, contact_repository: ContactRepository, notification_service: ContactNotificationService):
        self.contact_repository = contact_repository
        self.notification_service = notification_service

    def create(
        self,
        email: str,
        phone: str
    ) -> ContactModel:
        # Reglas de negocio: validar si el contacto ya existe
        existing_contact = self.contact_repository.find_by_email_or_phone(email, phone)
        if existing_contact:
            raise ContactAlreadyExistsException(f"Contact with email '{email}' or phone '{phone}' already exists")

        # Validar reglas de negocio sobre el formato de email y teléfono
        if not self._validate_email(email):
            raise InvalidContactDataException(f"Invalid email format: {email}")
        if not self._validate_phone(phone):
            raise InvalidContactDataException(f"Invalid phone format: {phone}")

        # Crear el nuevo contacto
        new_contact_model = ContactModel(
            email=email,
            phone=phone
        )

        self.contact_repository.save(new_contact_model)

        # Notificar la creación del contacto al servicio externo a través del puerto
        self.notification_service.notify_contact_creation(new_contact_model.id, new_contact_model.email)

        return new_contact_model

    def _validate_email(self, email: str) -> bool:
        """Validar si el formato de email es válido."""
        return '@' in email and '.' in email

    def _validate_phone(self, phone: str) -> bool:
        """Validar si el formato del teléfono es válido (longitud o caracteres permitidos)."""
        return phone.isdigit() and len(phone) <= 20
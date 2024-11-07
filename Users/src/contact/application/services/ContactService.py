from src.contact.application.useCases.ContactCreator import ContactCreator
from src.contact.domain.EventPublisher import EventPublisher
from src.contact.domain.ContactRepository import ContactRepository

class contact_service:
    def __init__(self, contact_repository: ContactRepository, publisher: EventPublisher):
        self.contact_creator = ContactCreator(contact_repository)
        self.publisher = publisher
    
    def create_contact(self, contact_id: int, email: str, phone: str, name: str, last_name: str):
        contact_model = self.contact_creator.create(email, phone, name, last_name)
        event = {"email": contact_model.email, "phone": contact_model.phone}
        self.publisher.publish(event)
        return contact_model
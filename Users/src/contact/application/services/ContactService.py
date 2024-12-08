from src.contact.application.useCases.ContactCreator import ContactCreator
from src.contact.domain.ContactRepository import ContactRepository
from src.contact.domain.EventPublisher import EventPublisher

class ContactService:
    def __init__(self, contact_repository: ContactRepository, publisher: EventPublisher):
        self.contact_creator = ContactCreator(contact_repository)
        self.contact_repository = contact_repository
        self.publisher = publisher
        
    def create_contact(self, name: str, last_name: str, email:str, phone: str):
        new_contact = self.contact_creator.create(email, phone, name, last_name)
        event = {"id": new_contact.id, "email": new_contact.email, "phone": new_contact.phone, "name": new_contact.name, "last_name": new_contact.last_name}
        self.publisher.publish(event)
        return new_contact
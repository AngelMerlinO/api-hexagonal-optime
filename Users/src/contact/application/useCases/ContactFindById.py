from src.contact.domain.ContactRepository import ContactRepository
from src.contact.domain.Contact import Contact

class ContactFindByID:
    def __init__(self, contact_repository: ContactRepository):
        self.contact_repository = contact_repository
        
    def find_by_id(self, contact_id: int) -> Contact:
        contact = self.contact_repository.find_by_id(contact_id)
        
        if not contact:
            raise ValueError(f"Contact with ID {contact_id} not found.")
        
        return contact  

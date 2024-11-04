import uuid
from src.users.domain.UserRepository import UserRepository
from src.contact.domain.ContactRepository import ContactRepository
from src.users.domain.User import User

class UserCreator:
    def __init__(self, user_repository: UserRepository, contact_repository: ContactRepository):
        self.user_repository = user_repository
        self.contact_repository = contact_repository
        

    def create(self,contact_id: int, username: str, email: str, password: str):
        
        new_user = User(
            uuid=str(uuid.uuid4()),
            contact_id=contact_id,
            username=username, 
            email=email, 
            password=password
            )
        self.user_repository.save(new_user)
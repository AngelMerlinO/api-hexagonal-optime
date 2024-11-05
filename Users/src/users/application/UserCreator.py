# Users/src/users/application/UserCreator.py
import uuid
from src.users.domain.UserRepository import UserRepository
from src.contact.domain.ContactRepository import ContactRepository
from src.users.domain.User import User
from src.users.domain.EventPublisher import EventPublisher

class UserCreator:
    def __init__(self, user_repository: UserRepository, contact_repository: ContactRepository, publisher: EventPublisher):
        self.user_repository = user_repository
        self.contact_repository = contact_repository
        self.publisher = publisher

    def create(self, contact_id: int, username: str, email: str, password: str):
        new_user = User(
            uuid=str(uuid.uuid4()),
            contact_id=contact_id,
            username=username, 
            email=email, 
            password=password
        )
        
        # Guardar el usuario en el repositorio
        self.user_repository.save(new_user)

        # Publicar el evento de "Usuario Creado" en la cola
        event = {"uuid": new_user.uuid, "username": new_user.username, "email": new_user.email}
        self.publisher.publish(event)
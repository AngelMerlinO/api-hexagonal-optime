import uuid
from src.users.domain.UserRepository import UserRepository
from src.users.domain.User import User

class UserCreator:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create(self, username: str, email: str, password: str):
        new_user = User(
            uuid=str(uuid.uuid4()),
            username=username, 
            email=email, 
            password=password
            )
        self.user_repository.save(new_user)
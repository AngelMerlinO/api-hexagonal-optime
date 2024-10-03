from src.users.domain.UserRepository import UserRepository
from src.users.domain.User import User

class UserUpdater:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def update(self, user_id: int, username: str = None, email: str = None, password: str = None):
        user = self.user_repository.find_by_id(user_id)
        
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Actualizamos solo los campos proporcionados
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = password

        self.user_repository.update(user)
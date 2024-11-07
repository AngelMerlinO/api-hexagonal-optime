from src.users.domain.UserRepository import UserRepository
from src.users.domain.User import User

class UserUpdater:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def update(self, identifier: str, username: str = None, password: str = None):
        user = self.user_repository.find_by_id(int(identifier))

        if not user:
            raise ValueError(f"User with ID {identifier} not found.")

        # Actualizar los valores si se proporcionan
        self.user_repository.update_by_id(
            id=int(identifier),
            username=username if username else user.username,
            password=password if password else user.password
        )
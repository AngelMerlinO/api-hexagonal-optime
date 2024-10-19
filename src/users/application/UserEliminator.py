from src.users.domain.UserRepository import UserRepository
from src.users.domain.User import User

class UserEliminator:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def delete(self, identifier: str):
        user = self.user_repository.find_by_id(int(identifier))

        if not user:
            raise ValueError(f"User with ID {identifier} not found.")

        self.user_repository.delete(user)

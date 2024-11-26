from src.users.domain.UserRepository import UserRepository
from src.users.domain.User import User

class UserFindById:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def find_by_identifier(self, identifier: str) -> dict:
        user_with_contact = self.user_repository.find_by_id(int(identifier))

        if not user_with_contact:
            raise ValueError(f"User with ID {identifier} not found.")

        return user_with_contact

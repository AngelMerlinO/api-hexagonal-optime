from src.users.domain.UserRepository import UserRepository
from src.users.domain.User import User

class UserEliminator:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    def delete(self, user_id: int):
        user = self.user_repository.find_by_id(user_id)
        
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        
        self.user_repository.delete(user)
        
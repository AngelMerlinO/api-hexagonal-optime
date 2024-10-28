from abc import ABC, abstractmethod
from .User import User
from typing import Optional

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User):
        """Guarda un usuario en el repositorio."""
        pass

    @abstractmethod
    def update_by_id(self, id: int, username: Optional[str], email: Optional[str], password: Optional[str]):
        """Actualiza los datos de un usuario por su ID."""
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> User:
        """Encuentra un usuario por su ID."""
        pass

    @abstractmethod
    def delete_by_id(self, user_id: int):
        """Elimina un usuario del repositorio por su ID."""
        pass


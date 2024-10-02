from abc import ABC, abstractmethod
from .User import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User):
        """Guarda un usuario en el repositorio"""
        pass

    @abstractmethod
    def update(self, user: User):
        """Actualiza los datos de un usuario en el repositorio"""
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> User:
        """Encuentra un usuario por su ID"""
        pass
    
    @abstractmethod
    def delete(self, user: User):
        """Elimina un usuario del repositorio"""
        pass
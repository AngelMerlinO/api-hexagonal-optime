from abc import ABC, abstractmethod
from .Contact import Contact
from typing import Optional, List

class ContactRepository(ABC):
    @abstractmethod
    def save(self, contact: Contact):
        """Guarda un contacto en el repositorio."""
        pass

    @abstractmethod
    def update_by_id(self, contact_id: int, email: Optional[str], phone: Optional[str], name: Optional[str], last_name: Optional[str]):
        """Actualiza los datos de un contacto por su ID."""
        pass

    @abstractmethod
    def find_by_id(self, contact_id: int) -> Optional[Contact]:
        """Encuentra un contacto por su ID."""
        pass

    @abstractmethod
    def delete_by_id(self, contact_id: int):
        """Elimina un contacto del repositorio por su ID (soft delete o eliminación lógica)."""
        pass

    @abstractmethod
    def find_all(self) -> List[Contact]:
        """Devuelve todos los contactos no eliminados."""
        pass

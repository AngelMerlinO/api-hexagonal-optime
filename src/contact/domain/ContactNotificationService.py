from abc import ABC, abstractmethod

class ContactNotificationService(ABC):
    @abstractmethod
    def notify_contact_creation(self, contact_id: int, email: str):
        """Notifica la creación de un contacto a un servicio externo."""
        pass
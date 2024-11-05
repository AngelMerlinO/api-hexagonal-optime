# Users/src/users/domain/EventPublisher.py
from abc import ABC, abstractmethod

class EventPublisher(ABC):
    @abstractmethod
    def publish(self, message: dict):
        """Publica un evento en una cola o sistema de mensajería."""
        pass
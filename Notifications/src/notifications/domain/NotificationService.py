# Notifications/src/notifications/domain/NotificationService.py

from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, user_id: int, title: str, message: str):
        pass
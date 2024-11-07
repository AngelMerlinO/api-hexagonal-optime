# Notifications/src/notifications/domain/NotificationFactory.py

from src.notifications.domain.NotificationService import NotificationService
from abc import ABC

class NotificationFactory(ABC):
    def get_notification_service(self, service_type: str) -> NotificationService:
        raise NotImplementedError("Este método debe implementarse en una subclase")
# Notifications/src/notifications/infrastructure/NotificationFactoryImpl.py

from src.notifications.domain.NotificationFactory import NotificationFactory
from src.notifications.domain.NotificationService import NotificationService
from src.notifications.infrastructure.externalService.EmailNotificationService import EmailNotificationService
from src.notifications.infrastructure.externalService.WhatsAppNotificationService import WhatsAppNotificationService

class NotificationFactoryImpl(NotificationFactory):
    def get_notification_service(self, service_type: str) -> NotificationService:
        if service_type == "email":
            return EmailNotificationService()
        elif service_type == "whatsapp":
            return WhatsAppNotificationService()
        else:
            raise ValueError(f"Tipo de notificación no soportado: {service_type}")
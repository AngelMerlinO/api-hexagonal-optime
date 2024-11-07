# Notifications/src/notifications/application/useCases/NotificationCreator.py

from src.notifications.domain.NotificationRepository import NotificationRepository
from src.notifications.domain.Notification import Notification, NotificationType
from src.notifications.domain.exceptions import InvalidNotificationTypeException
from src.notifications.domain.NotificationFactory import NotificationFactory  # Importar la fábrica
import uuid
from datetime import datetime, timezone

class NotificationCreator:
    def __init__(self, notification_repository: NotificationRepository, notification_factory: NotificationFactory):
        self.notification_repository = notification_repository
        self.notification_factory = notification_factory  # Fábrica para obtener servicios de notificación

    def create(self, user_id: int, title: str, message: str, type: str, service_type: str, link: str = None):
        # Validación del tipo de notificación
        if type not in NotificationType.__members__:
            raise InvalidNotificationTypeException(f"Invalid notification type: {type}")

        # Crear instancia de Notification con un nuevo uuid
        notification = Notification(
            user_id=user_id,
            uuid=str(uuid.uuid4()),
            title=title,
            message=message,
            type=NotificationType[type],
            link=link,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            deleted_at=None
        )

        # Guardar la notificación en el repositorio
        saved_notification = self.notification_repository.save(notification)

        # Obtener el servicio de notificación adecuado
        notification_service = self.notification_factory.get_notification_service(service_type)
        
        # Enviar la notificación
        notification_service.send_notification(user_id, title, message)

        return saved_notification
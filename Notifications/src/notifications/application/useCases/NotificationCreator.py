from src.notifications.domain.NotificationRepository import NotificationRepository
from src.notifications.domain.Notification import Notification, NotificationType
from src.notifications.domain.exceptions import InvalidNotificationTypeException
import uuid
from datetime import datetime, timezone

class NotificationCreator:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def create(self, user_id: int, title: str, message: str, type: str, link: str = None):
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

        # Guardar la notificación en el repositorio de MongoDB
        saved_notification = self.notification_repository.save(notification)
        return saved_notification

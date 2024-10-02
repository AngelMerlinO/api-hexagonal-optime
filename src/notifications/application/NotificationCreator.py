from src.notifications.domain.NotificationRepository import NotificationRepository
from src.users.domain.UserRepository import UserRepository
from src.notifications.domain.Notification import Notification, NotificationType
from src.users.domain.exceptions import UserNotFoundException
from src.notifications.domain.exceptions import InvalidNotificationTypeException

class NotificationCreator:
    def __init__(self, notification_repository: NotificationRepository, user_repository: UserRepository):
        self.notification_repository = notification_repository
        self.user_repository = user_repository

    def create(self, user_id: int, title: str, message: str, type: str, link: str = None):
        # Verificar si el usuario existe
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} does not exist")

        # Validar el tipo de notificación
        if type not in NotificationType.__members__:
            raise InvalidNotificationTypeException(f"Invalid notification type: {type}")

        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=NotificationType[type],
            link=link
        )

        self.notification_repository.save(notification)
        return notification
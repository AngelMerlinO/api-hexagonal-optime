from src.notifications.domain.NotificationRepository import NotificationRepository
from src.notifications.domain.Notification import Notification

class NotificationEliminator:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository
        
    def delete(self, notification_id: str):
        notification = self.notification_repository.find_by_id(notification_id)
        
        if not notification:
            raise ValueError(f"Notification with ID {notification_id} not found.")
        
        self.notification_repository.delete(notification)
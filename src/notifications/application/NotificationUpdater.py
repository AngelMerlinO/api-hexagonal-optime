from src.notifications.domain.NotificationRepository import NotificationRepository
from src.notifications.domain.Notification import Notification

class NotificationUpdater:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository
        
    def update(self, notification_id: int, title: str = None, message: str=None, type: str=None, link: str=None):
        notifications = self.notification_repository.find_by_id(notification_id)
        
        if not notifications:
            raise ValueError(f"Notification with ID {notification_id} not found.")
        
        if title:
            notifications.title = title
        if message:
            notifications.message = message
        if type:
            notifications.type = type
        if link:
            notifications.link = link
        
        self.notification_repository.update(notifications)
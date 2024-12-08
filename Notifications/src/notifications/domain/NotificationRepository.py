from abc import ABC, abstractmethod
from typing import List
from .Notification import Notification

class NotificationRepository(ABC):
    @abstractmethod
    def save(self, notification: Notification):
        pass

    @abstractmethod
    def find_by_id(self, notification_id: str) -> Notification:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Notification]:
        pass
    
    @abstractmethod
    def update(self, notification_id: str) -> Notification:
        pass

    @abstractmethod
    def delete(self, notification: Notification):
        pass
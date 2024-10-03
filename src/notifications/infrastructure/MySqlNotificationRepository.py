from src.notifications.domain.NotificationRepository import NotificationRepository
from src.notifications.domain.Notification import Notification
from sqlalchemy.orm import Session
from typing import List

class MySqlNotificationRepository(NotificationRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, notification: Notification):
        self.db_session.add(notification)
        self.db_session.commit()
        self.db_session.refresh(notification)
        return notification

    def find_by_id(self, notification_id: int) -> Notification:
        notification = self.db_session.query(Notification).filter_by(id=notification_id).first()
        return notification

    def find_by_user_id(self, user_id: int) -> List[Notification]:
        notifications = self.db_session.query(Notification).filter_by(user_id=user_id).all()
        return notifications

    def update(self, notification: Notification):
        self.db_session.merge(notification)
        self.db_session.commit()

    def delete(self, notification: Notification):
        self.db_session.delete(notification)
        self.db_session.commit()
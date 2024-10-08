from src.notifications.domain.NotificationRepository import NotificationRepository
from src.notifications.infrastructure.orm.NotificationModel import NotificationModel
from sqlalchemy.orm import Session
from typing import List

class MySqlNotificationRepository(NotificationRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, notification: NotificationModel):
        self.db_session.add(notification)
        self.db_session.commit()
        self.db_session.refresh(notification)
        return notification

    def find_by_id(self, notification_id: int) -> NotificationModel:
        return self.db_session.query(NotificationModel).filter_by(id=notification_id).first()

    def find_by_user_id(self, user_id: int) -> List[NotificationModel]:
        return self.db_session.query(NotificationModel).filter_by(user_id=user_id).all()

    def update(self, notification: NotificationModel):
        self.db_session.merge(notification)  # Usar merge para combinar el objeto actualizado
        self.db_session.commit()
        self.db_session.refresh(notification)  # Refrescar el objeto para obtener los últimos cambios
        return notification

    def delete(self, notification: NotificationModel):
        self.db_session.delete(notification)
        self.db_session.commit()
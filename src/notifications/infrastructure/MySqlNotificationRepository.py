from src.notifications.domain.NotificationRepository import NotificationRepository
from src.notifications.infrastructure.orm.NotificationModel import NotificationModel
from src.notifications.domain.Notification import Notification, NotificationType, NotificationStatus
from sqlalchemy.orm import Session
from typing import List

class MySqlNotificationRepository(NotificationRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, notification: Notification):
        notification_model = NotificationModel(
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
            type=notification.type.value,
            status=notification.status.value,
            link=notification.link
        )
        self.db_session.add(notification_model)
        self.db_session.commit()
        self.db_session.refresh(notification_model)

        notification.id = notification_model.id
        return notification

    def find_by_id(self, notification_id: int) -> Notification:
        notification_model = self.db_session.query(NotificationModel).filter_by(id=notification_id).first()
        if not notification_model:
            raise ValueError(f"Notification with ID {notification_id} not found")
        
        # Convertir el modelo de infraestructura a objeto de dominio
        return Notification(
            id=notification_model.id,
            user_id=notification_model.user_id,
            title=notification_model.title,
            message=notification_model.message,
            # Convertir el enum de infraestructura a dominio
            type=NotificationType(notification_model.type.name),  # Convertir por el nombre
            status=NotificationStatus(notification_model.status.name),  # Convertir por el nombre
            link=notification_model.link
        )

    def find_by_user_id(self, user_id: int) -> List[Notification]:
        notification_models = self.db_session.query(NotificationModel).filter_by(user_id=user_id).all()

        notifications = [
            Notification(
                id=notification_model.id,
                user_id=notification_model.user_id,
                title=notification_model.title,
                message=notification_model.message,
                type=NotificationType(notification_model.type),
                status=NotificationStatus(notification_model.status),
                link=notification_model.link
            )
            for notification_model in notification_models
        ]

        return notifications

    def update(self, notification: Notification):
        notification_model = self.db_session.query(NotificationModel).filter_by(id=notification.id).first()
        if not notification_model:
            raise ValueError(f"Notification with ID {notification.id} not found")
        
        notification_model.title = notification.title
        notification_model.message = notification.message
        notification_model.type = notification.type.value
        notification_model.status = notification.status.value
        notification_model.link = notification.link

        self.db_session.commit()
        self.db_session.refresh(notification_model)
        return notification

    def delete(self, notification: Notification):
        notification_model = self.db_session.query(NotificationModel).filter_by(id=notification.id).first()
        if not notification_model:
            raise ValueError(f"Notification with ID {notification.id} not found")
        
        self.db_session.delete(notification_model)
        self.db_session.commit()

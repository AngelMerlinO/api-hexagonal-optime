from src.notifications.domain.NotificationRepository import NotificationRepository
from src.notifications.domain.Notification import Notification, NotificationType, NotificationStatus
from pymongo.collection import Collection
from typing import List
from bson.objectid import ObjectId
from datetime import datetime, timezone

class MongoNotificationRepository(NotificationRepository):
    def __init__(self, db_collection: Collection):
        self.collection = db_collection

    def save(self, notification: Notification):
        notification_data = {
            "uuid": notification.uuid,
            "user_id": notification.user_id,
            "title": notification.title,
            "message": notification.message,
            "type": notification.type.value,
            "status": notification.status.value,
            "link": notification.link,
            "created_at": (notification.created_at or datetime.now()).astimezone(timezone.utc),
            "updated_at": None,
            "deleted_at": None,
        }
        result = self.collection.insert_one(notification_data)
        notification.id = str(result.inserted_id)
        return notification

    def find_by_id(self, notification_id: str) -> Notification:
        # Buscar un documento por ID en MongoDB
        notification_data = self.collection.find_one({"_id": ObjectId(notification_id)})
        if not notification_data:
            raise ValueError(f"Notification with ID {notification_id} not found")

        return Notification(
            id=str(notification_data["_id"]),
            uuid=notification_data["uuid"],
            user_id=notification_data["user_id"],
            title=notification_data["title"],
            message=notification_data["message"],
            type=NotificationType(notification_data["type"]),
            status=NotificationStatus(notification_data["status"]),
            link=notification_data.get("link"),
            created_at=notification_data.get("created_at", datetime.now().astimezone(timezone.utc)),
            updated_at=notification_data.get("updated_at", datetime.now().astimezone(timezone.utc)),
            deleted_at=notification_data.get("deleted_at")
        )

    def find_by_user_id(self, user_id: int) -> List[Notification]:
        # Buscar documentos por user_id en MongoDB
        notification_models = self.collection.find({"user_id": user_id})
        
        notifications = [
            Notification(
                id=str(notification["_id"]),
                uuid=notification["uuid"],
                user_id=notification["user_id"],
                title=notification["title"],
                message=notification["message"],
                type=NotificationType(notification["type"]),
                status=NotificationStatus(notification["status"]),
                link=notification.get("link"),
                created_at=notification.get("created_at", datetime.now().astimezone(timezone.utc)),
                updated_at=notification.get("updated_at", datetime.now().astimezone(timezone.utc)),
                deleted_at=notification.get("deleted_at")
            )
            for notification in notification_models
        ]

        return notifications

    def update(self, notification: Notification):
        result = self.collection.update_one(
            {"_id": ObjectId(notification.id)},
            {"$set": {
                "title": notification.title,
                "message": notification.message,
                "type": notification.type.value,
                "status": notification.status.value,
                "link": notification.link,
                "updated_at": datetime.now(timezone.utc)
            }}
        )
        if result.matched_count == 0:
            raise ValueError(f"Notification with ID {notification.id} not found")
        return notification

    def delete(self, notification: Notification):
        result = self.collection.delete_one({"_id": ObjectId(notification.id)})
        if result.deleted_count == 0:
            raise ValueError(f"Notification with ID {notification.id} not found")

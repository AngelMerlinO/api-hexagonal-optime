from pymongo.collection import Collection
from fastapi import Depends
from src.notifications.infrastructure.MySqlNotificationRepository import MongoNotificationRepository
from src.notifications.application.services.NotificationService import NotificationService
from config.database import get_mongo_collection  # Función que retorna la colección de MongoDB

def get_notification_service(db: Collection = Depends(get_mongo_collection)) -> NotificationService:
    # Crear instancias de los repositorios usando la colección de MongoDB
    notification_repository = MongoNotificationRepository(db)
    
    # Crear instancia de NotificationService usando los repositorios
    notification_service = NotificationService(
        notification_repository=notification_repository
    )
    
    return notification_service
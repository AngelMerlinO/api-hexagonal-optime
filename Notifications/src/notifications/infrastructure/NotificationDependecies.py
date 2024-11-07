# Notifications/src/notifications/infrastructure/NotificationDependecies.py

from fastapi import Depends
from pymongo.collection import Collection
from src.notifications.infrastructure.MySqlNotificationRepository import MongoNotificationRepository
from src.notifications.application.useCases.NotificationCreator import NotificationCreator
from src.notifications.domain.NotificationRepository import NotificationRepository
from src.notifications.infrastructure.NotificationFactoryImpl import NotificationFactoryImpl
from config.database import get_mongo_collection

def get_notification_creator(db: Collection = Depends(get_mongo_collection)) -> NotificationCreator:
    # Crear el repositorio de notificación
    notification_repository = MongoNotificationRepository(db)
    
    # Crear la fábrica de notificaciones que maneja distintos servicios
    notification_factory = NotificationFactoryImpl()
    
    # Instanciar y devolver NotificationCreator con las dependencias configuradas
    return NotificationCreator(notification_repository=notification_repository, notification_factory=notification_factory)
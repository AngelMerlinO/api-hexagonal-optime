# Notifications/src/notifications/infrastructure/NotificationDependecies.py

from fastapi import Depends
from pymongo.collection import Collection
from src.notifications.infrastructure.MySqlNotificationRepository import MongoNotificationRepository
from src.notifications.application.useCases.NotificationCreator import NotificationCreator
from src.notifications.application.useCases.NotificationUpdater import NotificationUpdater
from src.notifications.application.useCases.NotificationEliminator import NotificationEliminator
from src.notifications.domain.NotificationRepository import NotificationRepository
from src.notifications.infrastructure.NotificationFactoryImpl import NotificationFactoryImpl
from config.database import get_mongo_collection

def get_notification_creator(db: Collection = Depends(get_mongo_collection)) -> NotificationCreator:
    notification_repository = MongoNotificationRepository(db)
    notification_factory = NotificationFactoryImpl()
    return NotificationCreator(notification_repository=notification_repository, notification_factory=notification_factory)

def get_notification_updater(db: Collection = Depends(get_mongo_collection)) -> NotificationUpdater:
    notification_repository = MongoNotificationRepository(db)
    return NotificationUpdater(notification_repository=notification_repository)

def get_notification_eliminator(db: Collection = Depends(get_mongo_collection)) -> NotificationEliminator:
    notification_repository = MongoNotificationRepository(db)
    return NotificationEliminator(notification_repository=notification_repository)
from src.notifications.application.useCases.NotificationCreator import NotificationCreator
from src.notifications.application.useCases.NotificationUpdater import NotificationUpdater
from src.notifications.application.useCases.NotificationEliminator import NotificationEliminator
from src.notifications.domain.NotificationRepository import NotificationRepository
from src.notifications.infrastructure.NotificationFactoryImpl import NotificationFactoryImpl

class NotificationService:
    def __init__(self, notification_repository: NotificationRepository):
        notification_factory = NotificationFactoryImpl()
        self.notification_creator = NotificationCreator(notification_repository, notification_factory)
        self.notification_updater = NotificationUpdater(notification_repository)
        self.notification_eliminator = NotificationEliminator(notification_repository)
        self.notification_repository = notification_repository

    def create_notification(self, user_id: int, title: str, content: str, type: str, service_type: str, link: str = None):
        self.notification_creator.create(user_id, title, content, type, service_type, link)

    def update_notification(self, identifier: str, title: str = None, content: str = None, type: str = None, link: str = None):
        self.notification_updater.update(identifier, title=title, message=content, type=type, link=link)

    def delete_notification(self, identifier: str):
        try:
            self.notification_eliminator.delete(identifier)
        except ValueError as e:
            # Manejar el caso en que la notificación no se encuentre
            print(f"Error: {str(e)}")

    def get_notification_by_id(self, notification_id: str):
        # Utiliza el repositorio para buscar la notificación
        return self.notification_repository.find_by_id(notification_id)
from src.users.application.useCases.UserCreatorUseCase import UserCreator
from src.users.application.useCases.UserUpdater import UserUpdater
from src.users.application.useCases.UserFindById import UserFindById
from src.users.application.useCases.UserEliminator import UserEliminator
from src.users.domain.UserRepository import UserRepository
from src.contact.domain.ContactRepository import ContactRepository
from src.users.domain.EventPublisher import EventPublisher

class UserService:
    def __init__(self, user_repository: UserRepository, contact_repository: ContactRepository, publisher: EventPublisher):
        self.user_creator = UserCreator(user_repository, contact_repository)
        self.user_updater = UserUpdater(user_repository)
        self.user_eliminator = UserEliminator(user_repository)
        self.user_repository = user_repository
        self.publisher = publisher

    def create_user(self, contact_id: int, username: str, password: str):
        new_user = self.user_creator.create(contact_id, username,  password)
        event = {"uuid": new_user.uuid, "username": new_user.username, "password": new_user.password}
        self.publisher.publish(event)
        return new_user

    def update_user(self, identifier: str, username: str = None, password: str = None):
        self.user_updater.update(identifier, username, password)

    def delete_user(self, identifier: str):
        self.user_eliminator.delete(identifier)

    def user_by_id(self, identifier: str):
        user_finder = UserFindById(self.user_repository)
        return user_finder.find_by_identifier(identifier)
    
    def user_by_username(self, username: str):
        return self.user_repository.find_by_username(username)
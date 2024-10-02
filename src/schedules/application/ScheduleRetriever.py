from src.schedules.domain.ScheduleRepository import ScheduleRepository
from src.users.domain.UserRepository import UserRepository
from src.users.domain.exceptions import UserNotFoundException
from src.schedules.domain.exceptions import ScheduleNotFoundException

class ScheduleRetriever:
    def __init__(self, schedule_repository: ScheduleRepository, user_repository: UserRepository):
        self.schedule_repository = schedule_repository
        self.user_repository = user_repository

    def get_by_user_id(self, user_id: int):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} does not exist")

        schedules = self.schedule_repository.find_by_user_id(user_id)
        if not schedules:
            raise ScheduleNotFoundException(f"No schedules found for user with id {user_id}")

        return schedules
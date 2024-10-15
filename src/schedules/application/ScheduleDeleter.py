from src.schedules.domain.ScheduleRepository import ScheduleRepository
from src.users.domain.UserRepository import UserRepository
from src.schedules.domain.exceptions import ScheduleNotFoundException
from src.users.domain.exceptions import UserNotFoundException

class ScheduleDeleter:
    def __init__(self, schedule_repository: ScheduleRepository, user_repository: UserRepository):
        self.schedule_repository = schedule_repository
        self.user_repository = user_repository

    def delete(self, schedule_uuid: str, user_uuid: str):
        user = self.user_repository.find_by_id(user_uuid)
        if not user:
            raise UserNotFoundException(f"User with id {user_uuid} does not exist")

        schedule = self.schedule_repository.find_by_id(schedule_uuid)
        if not schedule:
            raise ScheduleNotFoundException(f"Schedule with id {schedule_uuid} does not exist")

        if schedule.user_id != user.id:
            raise PermissionError("User does not have permission to delete this schedule")

        self.schedule_repository.delete(schedule)
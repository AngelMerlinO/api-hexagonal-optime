from src.schedules.domain.schedule import Schedule
from src.schedules.domain.scheduleRepository import ScheduleRepository


class SchedulesUpdater:
    def __init__(self, schedule_repo: ScheduleRepository):
        self.schedule_repo = schedule_repo

    def update(self, schedule_id: int, updated_data: dict) -> Schedule:
        return self.schedule_repo.update(schedule_id, updated_data)

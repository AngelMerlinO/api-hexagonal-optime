from src.schedules.domain.scheduleRepository import ScheduleRepository
from src.schedules.domain.schedule import Schedule
from src.schedules.infraestructure.orm.scheduleModel import SchedulesModel

class SchedulesCreator:
    def __init__(self, schedule_repo: ScheduleRepository):
        self.schedule_repo = schedule_repo
    
    def create(self, schedule: Schedule) -> Schedule:
        if not schedule.user_id:
            raise ValueError("User ID is required to create a schedule.")
        
        created_schedule = self.schedule_repo.save(schedule)
        
        return created_schedule




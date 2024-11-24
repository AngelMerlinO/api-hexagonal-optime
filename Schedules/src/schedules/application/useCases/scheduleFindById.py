from src.schedules.domain.scheduleRepository import ScheduleRepository

class SchedulesFindById:
    def __init__(self, schedule_repo: ScheduleRepository):
        self.schedule_repo = schedule_repo
    
    def find_by_id(self, schedule_id: int):
        schedule = self.schedule_repo.find_by_id(schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} does not exist.")
        
        return schedule
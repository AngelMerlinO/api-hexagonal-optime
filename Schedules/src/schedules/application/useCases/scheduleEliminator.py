from src.schedules.domain.scheduleRepository import ScheduleRepository

class SchedulesEliminator:
    def __init__(self, schedule_repo: ScheduleRepository):
        self.schedule_repo = schedule_repo
    
    def delete(self, schedule_id: int):
        schedule = self.schedule_repo.find_by_id(schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} does not exist")
        
        self.schedule_repo.delete(schedule_id)
        
        
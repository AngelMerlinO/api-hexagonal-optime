from src.schedules.domain.ScheduleRepository import ScheduleRepository
from src.schedules.domain.Schedule import Schedule
from sqlalchemy.orm import Session

class MySqlScheduleRepository(ScheduleRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, schedule: Schedule):
        self.db_session.add(schedule)
        self.db_session.commit()
        self.db_session.refresh(schedule)
        return schedule

    def find_by_user_id(self, user_id: int) -> Schedule:
        schedule = self.db_session.query(Schedule).filter_by(user_id=user_id).first()
        return schedule

    def find_by_id(self, schedule_id: int) -> Schedule:
        schedule = self.db_session.query(Schedule).filter_by(id=schedule_id).first()
        return schedule

    def delete(self, schedule: Schedule):
        self.db_session.delete(schedule)
        self.db_session.commit()
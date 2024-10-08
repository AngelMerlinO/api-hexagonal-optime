from src.schedules.domain.ScheduleRepository import ScheduleRepository
from src.schedules.domain.Schedule import Schedule
from sqlalchemy.orm import Session
from typing import List

class MySqlScheduleRepository(ScheduleRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, schedule: Schedule):
        self.db_session.add(schedule)
        self.db_session.commit()
        self.db_session.refresh(schedule)
        return schedule

    def find_by_user_id(self, user_id: int, skip: int = 0, limit: int = 3) -> List[Schedule]:
        schedules = self.db_session.query(Schedule).filter_by(user_id=user_id).offset(skip).limit(limit).all()
        if not schedules:
            raise ValueError(f"No schedules found for user_id {user_id}")
        return schedules
    
    def find_by_id(self, schedule_id: int) -> Schedule:
        schedule = self.db_session.query(Schedule).filter_by(id=schedule_id).first()
        return schedule

    def delete(self, schedule: Schedule):
        self.db_session.delete(schedule)
        self.db_session.commit()

    def update(self, schedule: Schedule):
        self.db_session.merge(schedule)
        self.db_session.commit()
        self.db_session.refresh(schedule)
        return schedule
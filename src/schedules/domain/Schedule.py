# src/schedules/domain/Schedule.py

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relación con User
    user = relationship('User', back_populates='schedules')

    # Relación con ScheduleItem
    schedule_items = relationship('ScheduleItem', back_populates='schedule', cascade='all, delete-orphan')

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"<Schedule {self.id} for User {self.user_id}>"
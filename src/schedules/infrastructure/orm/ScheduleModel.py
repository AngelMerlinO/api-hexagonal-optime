from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from config.database import Base
import uuid

class ScheduleModel(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('UserModel', back_populates='schedules')

    schedule_items = relationship('ScheduleItemModel', back_populates='schedule', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<ScheduleModel {self.id} for User {self.user_id}>"
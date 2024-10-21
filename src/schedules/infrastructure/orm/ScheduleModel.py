from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, composite
from config.database import Base
from src.schedules.domain.Timestamp import Timestamps
from sqlalchemy.sql import func
import uuid

class ScheduleModel(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, nullable=True)
    
    timestamps = composite(Timestamps, created_at, updated_at, deleted_at)

    user = relationship('UserModel', back_populates='schedules')
    schedule_items = relationship('ScheduleItemModel', back_populates='schedule', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<ScheduleModel {self.id} for User {self.user_id}>"
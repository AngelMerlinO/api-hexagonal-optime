from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship, composite
from sqlalchemy.sql import func
from config.database import Base
from src.schedules.domain.Timestamp import Timestamps
import uuid

class SchedulesModel(Base):
    __tablename__ = 'schedules'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    uuid = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, nullable=True)
    
    timestamps = composite(Timestamps, created_at, updated_at, deleted_at)
    subjects = relationship('SubjectModel', back_populates='schedules', cascade="all, delete-orphan")
    
    
    def __repr__(self):
        return f"<SchedulesModel {self.id} for User {self.user_id}>"
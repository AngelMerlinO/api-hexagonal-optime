from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, composite
from sqlalchemy.sql import func
from config.database import Base
from src.subject.domain.Timestamp import Timestamps
from sqlalchemy.dialects.mysql import JSON
import uuid

class SubjectModel(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    uuid = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    schedule_id = Column(Integer, ForeignKey('schedules.id'), nullable=False)
    name = Column(String(255), nullable=False)
    period = Column(Integer, nullable=False)
    group = Column(String(30), nullable=False)
    semester_grade = Column(Integer, nullable=False)
    serialization_raiting = Column(Integer, nullable=False)
    clearance_raiting = Column(Integer, nullable=False)
    monday = Column(JSON, nullable=True)
    tuesday = Column(JSON, nullable=True)
    wednesday = Column(JSON, nullable=True)
    thursday = Column(JSON, nullable=True)
    friday = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, nullable=True)
    
    timestamps =composite(Timestamps, created_at, updated_at, deleted_at)
    schedules = relationship('SchedulesModel', back_populates='subjects')
    
    def __repr__(self):
        return f"<SubjectsModel {self.name} for Schedule {self.schedule_id}>"
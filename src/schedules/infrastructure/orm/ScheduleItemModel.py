from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, composite
from sqlalchemy.dialects.mysql import JSON
from config.database import Base
from src.schedules.domain.Timestamp import Timestamps
from sqlalchemy.sql import func
import uuid


class ScheduleItemModel(Base):
    __tablename__ = 'schedule_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    schedule_id = Column(Integer, ForeignKey('schedules.id', ondelete='CASCADE'), nullable=False)
    nombre = Column(String(255), nullable=False)
    grupo = Column(String(50), nullable=True)
    cuatrimestre = Column(Integer, nullable=True)
    calif_cuatrimestre = Column(Integer, nullable=True)
    calif_holgura = Column(Integer, nullable=True)
    calif_seriacion = Column(Integer, nullable=True)
    lunes = Column(JSON, nullable=True)
    martes = Column(JSON, nullable=True)
    miercoles = Column(JSON, nullable=True)
    jueves = Column(JSON, nullable=True)
    viernes = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, nullable=True)
    
    timestamps = composite(Timestamps, created_at, updated_at, deleted_at)

    schedule = relationship('ScheduleModel', back_populates='schedule_items')

    def __repr__(self):
        return f"<ScheduleItemModel {self.nombre} in Schedule {self.schedule_id}>"
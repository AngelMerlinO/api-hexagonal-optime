from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import JSON
from config.database import Base

class ScheduleItemModel(Base):
    __tablename__ = 'schedule_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
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

    # Relación con ScheduleModel
    schedule = relationship('ScheduleModel', back_populates='schedule_items')

    def __repr__(self):
        return f"<ScheduleItemModel {self.nombre} in Schedule {self.schedule_id}>"
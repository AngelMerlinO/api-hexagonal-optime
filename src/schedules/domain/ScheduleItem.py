from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import JSON
from config.database import Base

class ScheduleItem(Base):
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

    # Relación con Schedule
    schedule = relationship('Schedule', back_populates='schedule_items')

    def __init__(self, nombre, grupo, cuatrimestre, calif_cuatrimestre, calif_holgura, calif_seriacion, lunes, martes, miercoles, jueves, viernes):
        self.nombre = nombre
        self.grupo = grupo
        self.cuatrimestre = cuatrimestre
        self.calif_cuatrimestre = calif_cuatrimestre
        self.calif_holgura = calif_holgura
        self.calif_seriacion = calif_seriacion
        self.lunes = lunes
        self.martes = martes
        self.miercoles = miercoles
        self.jueves = jueves
        self.viernes = viernes

    def __repr__(self):
        return f"<ScheduleItem {self.nombre} in Schedule {self.schedule_id}>"
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class ScheduleModel(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relación con UserModel usando el nombre de la clase como cadena
    user = relationship('UserModel', back_populates='schedules')

    # Relación con ScheduleItemModel
    schedule_items = relationship('ScheduleItemModel', back_populates='schedule', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<ScheduleModel {self.id} for User {self.user_id}>"
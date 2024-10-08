from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
from src.Activities.domain.Activities import ActivityType, ActivityStatus

class ActivitiesModel(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(Enum(ActivityType), nullable=False)
    status = Column(Enum(ActivityStatus), nullable=False, server_default='pending')
    delivery_date = Column(Date, nullable=False)
    link_classroom = Column(String(512), nullable=True)

    # Timestamps
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relación con UserModel, usando el nombre de la clase como cadena de texto
    user = relationship('UserModel', back_populates='activities')

    def __repr__(self):
        return f"<ActivitiesModel {self.title} for User {self.user_id}>"
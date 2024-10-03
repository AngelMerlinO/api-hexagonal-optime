from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum

# Definir los tipos de actividades como un enum
class ActivityType(enum.Enum):
    exam = 'exam'
    assignment = 'assignment'
    project = 'project'
    quiz = 'quiz'

# Definir los posibles estados de las actividades como un enum
class ActivityStatus(enum.Enum):
    sent = 'sent'
    pending = 'pending'
    completed = 'completed'
    overdue = 'overdue'

class Activities(Base):
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
    
    # Relación con la tabla de usuarios
    user = relationship("User", back_populates="activities")
    
    def __init__(self, user_id, title: str, description: str, type: ActivityType, delivery_date: Date, link_classroom: str, status: ActivityStatus):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.type = type
        self.delivery_date = delivery_date
        self.link_classroom = link_classroom
        self.status = status
    
    def __repr__(self):
        return f"<Activity {self.title} for User {self.user_id}>"

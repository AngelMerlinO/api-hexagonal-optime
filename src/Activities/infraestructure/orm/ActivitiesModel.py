from sqlalchemy import Column, Integer, String, Text, Date, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum
import uuid


class ActivityTypeEnum(enum.Enum):
    exam = 'exam'
    assignment = 'assignment'
    project = 'project'
    quiz = 'quiz'

class ActivityStatusEnum(enum.Enum):
    sent = 'sent'
    pending = 'pending'
    completed = 'completed'
    overdue = 'overdue'

class ActivitiesModel(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(Enum(ActivityTypeEnum), nullable=False)
    status = Column(Enum(ActivityStatusEnum), nullable=False, server_default='pending')
    delivery_date = Column(Date, nullable=False)
    link_classroom = Column(String(512), nullable=True)
    
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    user = relationship('UserModel', back_populates='activities')

    def __repr__(self):
        return f"<ActivitiesModel {self.title} for User {self.user_id}>"
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, composite
from config.database import Base
from src.users.domain.Timestamp import Timestamps
from sqlalchemy.sql import func   

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, nullable=True)
    
    timestamps = composite(Timestamps, created_at, updated_at, deleted_at)
    
    schedules = relationship('ScheduleModel', back_populates='user')
    notifications = relationship('NotificationModel', back_populates='user')
    activities = relationship('ActivitiesModel', back_populates='user')
    payments = relationship('PaymentModel', back_populates='user')
    contacts = relationship('ContactModel', back_populates='user')


    def __repr__(self):
        return f"<UserModel {self.username} ({self.email})>"
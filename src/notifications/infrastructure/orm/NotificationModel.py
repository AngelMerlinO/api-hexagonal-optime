from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum
import uuid

class NotificationTypeEnum(enum.Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'
    in_app = 'in-app'

class NotificationStatusEnum(enum.Enum):
    sent = 'sent'
    pending = 'pending'
    failed = 'failed'

class NotificationModel(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationTypeEnum), nullable=False)
    status = Column(Enum(NotificationStatusEnum), nullable=False, server_default='pending')
    link = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    user = relationship('UserModel', back_populates='notifications')

    def __repr__(self):
        return f"<NotificationModel {self.title} to User {self.user_id}>"

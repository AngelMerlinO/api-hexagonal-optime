from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum

class NotificationType(enum.Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'
    in_app = 'in-app'

class NotificationStatus(enum.Enum):
    sent = 'sent'
    pending = 'pending'
    failed = 'failed'

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    status = Column(Enum(NotificationStatus), nullable=False, server_default='pending')
    link = Column(String(255), nullable=True)
    sent_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relación con User
    user = relationship('User', back_populates='notifications')

    def __init__(self, user_id, title, message, type, link=None):
        self.user_id = user_id
        self.title = title
        self.message = message
        self.type = type
        self.link = link

    def __repr__(self):
        return f"<Notification {self.title} to User {self.user_id}>"
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipient_phone_number = Column(String(length=20), nullable=False)
    message_type = Column(String(length=50), nullable=False)  # e.g., "template", "text"
    message_content = Column(Text, nullable=False)
    status = Column(String(length=50), nullable=True)  # e.g., "sent", "failed"
    error_message = Column(Text, nullable=True)
    date_created = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    def __init__(self, recipient_phone_number, message_type, message_content, status=None, error_message=None):
        self.recipient_phone_number = recipient_phone_number
        self.message_type = message_type
        self.message_content = message_content
        self.status = status
        self.error_message = error_message

    def __repr__(self):
        return f"<Message {self.id} to {self.recipient_phone_number}>"
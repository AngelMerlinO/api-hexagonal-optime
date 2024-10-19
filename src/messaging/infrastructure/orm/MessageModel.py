from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from config.database import Base

class MessageModel(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipient_phone_number = Column(String(length=20), nullable=False)
    message_type = Column(String(length=50), nullable=False)
    message_content = Column(Text, nullable=False)
    status = Column(String(length=50), nullable=True)
    error_message = Column(Text, nullable=True)

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )
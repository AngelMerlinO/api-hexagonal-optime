from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, composite
from config.database import Base
from src.contact.domain.Timestamp import Timestamps
from sqlalchemy.sql import func


class ContactModel(Base):
    __tablename__ = 'contacts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, nullable=True)
    
    timestamps = composite(Timestamps, created_at, updated_at, deleted_at)
    
    user = relationship("UserModel", back_populates="contacts")
    
    def __repr__(self):
        return f"<ContactModel email='{self.email}' phone='{self.phone}'>"

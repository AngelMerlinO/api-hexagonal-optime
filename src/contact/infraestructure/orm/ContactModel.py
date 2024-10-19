from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from config.database import Base


class ContactModel(Base):
    __tablename__ = 'contacts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False, onupdate=func.current_timestamp())
    deleted_at = Column(TIMESTAMP, nullable=True)
    
    user = relationship("UserModel", back_populates="contacts")
    
    def __repr__(self):
        return f"<ContactModel email='{self.email}' phone='{self.phone}'>"

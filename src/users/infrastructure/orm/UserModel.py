import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)

    schedules = relationship('ScheduleModel', back_populates='user')
    notifications = relationship('NotificationModel', back_populates='user')
    activities = relationship('ActivitiesModel', back_populates='user')
    payments = relationship('PaymentModel', back_populates='user')
    contacts = relationship('ContactModel', back_populates='user')


    def __repr__(self):
        return f"<UserModel {self.username} ({self.email})>"
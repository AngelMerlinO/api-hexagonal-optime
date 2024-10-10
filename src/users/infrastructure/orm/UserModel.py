from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)

    schedules = relationship('ScheduleModel', back_populates='user')
    notifications = relationship('NotificationModel', back_populates='user')
    activities = relationship('ActivitiesModel', back_populates='user')
    payments = relationship('PaymentModel', back_populates='user')


    def __repr__(self):
        return f"<UserModel {self.username} ({self.email})>"
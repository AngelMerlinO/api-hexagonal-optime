from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Activities(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    delivery_date = Column(Date, nullable=False)
    link_classroom = Column(String(512), nullable=False)
    
    #Relacion con usuario
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="activities")
    
    def __init__(self, title: str, description: str, delivery_date: Date, link_classroom: str, user_id: int):
        self.title = title
        self.description = description
        self.delivery_date = delivery_date
        self.link_classroom = link_classroom
        self.user_id = user_id
    
    
    
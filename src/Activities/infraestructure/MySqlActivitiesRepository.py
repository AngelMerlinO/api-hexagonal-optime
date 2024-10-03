from typing import List
from src.Activities.domain.ActivitiesRepository import ActivitiesRepository
from src.Activities.domain.Activities import Activities
from sqlalchemy.orm import Session

class MySqlActivitiesRepository(ActivitiesRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def save(self, activities: Activities):
        self.db_session.add(activities)
        self.db_session.commit()
        self.db_session.refresh(activities) #Actualiza el ID del usuario después de guardarlo
        return activities
    
    def update(self, activities: Activities):
        self.db_session.merge(activities) #SQLAlchemy maneja las actualizaciones
        self.db_session.commit()
        
    def find_by_id(self, activities_id: int) -> Activities:
        return self.db_session.query(Activities).filter_by(id=activities_id).first()
    
    def find_by_user_id(self, user_id: int) -> List[Activities]:
        activities = self.db_session.query(Activities).filter_by(user_id=user_id).all()
        return activities
    
    def delete(self, activities: Activities):
        self.db_session.delete(activities)
        self.db_session.commit()
        return f"Activities with ID {activities.id} eliminated successfully."



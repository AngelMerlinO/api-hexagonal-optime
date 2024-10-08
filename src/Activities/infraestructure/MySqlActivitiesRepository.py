from typing import List
from src.Activities.domain.ActivitiesRepository import ActivitiesRepository
from src.Activities.infraestructure.orm.ActivitiesModel import ActivitiesModel
from sqlalchemy.orm import Session

class MySqlActivitiesRepository(ActivitiesRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def save(self, activities: ActivitiesModel):
        self.db_session.add(activities)
        self.db_session.commit()
        self.db_session.refresh(activities)
        return activities
    
    def update(self, activities: ActivitiesModel):
        self.db_session.merge(activities)
        self.db_session.commit()
        
    def find_by_id(self, activities_id: int) -> ActivitiesModel:
        return self.db_session.query(ActivitiesModel).filter_by(id=activities_id).first()
    
    def find_by_user_id(self, user_id: int) -> List[ActivitiesModel]:
        activities = self.db_session.query(ActivitiesModel).filter_by(user_id=user_id).all()
        return activities
    
    def delete(self, activities: ActivitiesModel):
        self.db_session.delete(activities)
        self.db_session.commit()
        return f"Activities with ID {activities.id} eliminated successfully."
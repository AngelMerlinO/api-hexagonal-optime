from src.Activities.domain.ActivitiesRepository import ActivitiesRepository
from src.Activities.domain.Activities import Activities

class ActivitiesFindByID:
    def __init__(self, activities_repository: ActivitiesRepository):
        self.activities_repository = activities_repository
        
    def find_by_id(self, activities_id: int) -> Activities:
        activities = self.activities_repository.find_by_id(activities_id)
        
        if not activities:
            raise ValueError(f"Activities with ID {activities_id} not found.")
        
        return activities  

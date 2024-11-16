from src.activities.domain.ActivitiesRepository import ActivitiesRepository
from src.activities.domain.Activities import Activities

class ActivitiesEliminator:
    def __init__(self, activities_repository: ActivitiesRepository):
        self.activities_repository = activities_repository
        
    def delete(self, activities_id: int):
        activity = self.activities_repository.find_by_id(activities_id)
        
        if not activity:
            raise ValueError(f"Activities with ID {activities_id} not found.")
        
        self.activities_repository.delete(activity)

from src.activities.domain.ActivitiesRepository import ActivitiesRepository
from src.activities.domain.Activities import Activities
from datetime import date

class ActivitiesUpdater:
    def __init__(self, activities_repository: ActivitiesRepository):
        self.activities_repository = activities_repository
        
    def update(self, activities_id: int, title: str = None, description: str = None, delivery_date: date = None, link_classroom: str = None):
        activities = self.activities_repository.find_by_id(activities_id)
        
        if not activities:
            raise ValueError(f"Activity with ID {activities_id} not found.")
        
        if title:
            activities.title = title
        if description:
            activities.description = description
        if delivery_date:
            activities.delivery_date = delivery_date
        if link_classroom:
            activities.link_classroom = link_classroom
        
        self.activities_repository.update(activities)
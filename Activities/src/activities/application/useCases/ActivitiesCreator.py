from datetime import date
import uuid
from src.activities.domain.ActivitiesRepository import ActivitiesRepository
from src.activities.domain.Activities import Activities, ActivityType, ActivityStatus
from src.activities.domain.exceptions import InvalidActivityTypeException, InvalidActivityStatusException
from src.activities.infraestructure.orm.ActivitiesModel import ActivityTypeEnum, ActivityStatusEnum, ActivitiesModel

class ActivitiesCreator:
    def __init__(self, activities_repository: ActivitiesRepository):
        self.activities_repository = activities_repository
        
    def create(
        self,
        title: str,
        description: str,
        delivery_date: date,
        link_classroom: str,
        user_id: int,
        activity_type: str,
        status: str
    ):
        
        if activity_type not in ActivityType.__members__:
            raise InvalidActivityTypeException(f"Invalid Activity type {activity_type}")
        
        if status not in ActivityStatus.__members__:
            raise InvalidActivityStatusException(f"Invalid Activity status {status}")
        
        new_activity_model = ActivitiesModel(
            uuid=str(uuid.uuid4()),
            title=title,
            description=description,
            delivery_date=delivery_date,
            link_classroom=link_classroom,
            user_id=user_id,
            type=ActivityTypeEnum[activity_type],
            status=ActivityStatusEnum[status]
        )
        
        self.activities_repository.save(new_activity_model)
        
        return new_activity_model 
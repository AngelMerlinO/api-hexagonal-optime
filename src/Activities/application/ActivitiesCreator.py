from datetime import date
import uuid
from src.Activities.domain.ActivitiesRepository import ActivitiesRepository
from src.Activities.domain.Activities import Activities, ActivityType, ActivityStatus
from src.users.domain.UserRepository import UserRepository
from src.users.domain.exceptions import UserNotFoundException
from src.Activities.domain.exceptions import InvalidActivityTypeException, InvalidActivityStatusException
from src.Activities.infraestructure.orm.ActivitiesModel import ActivityTypeEnum, ActivityStatusEnum, ActivitiesModel

class ActivitiesCreator:
    def __init__(self, activities_repository: ActivitiesRepository, user_repository: UserRepository):
        self.activities_repository = activities_repository
        self.user_repository = user_repository
        
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
        user = self.user_repository.find_by_id(user_id)
        if not user: 
            raise UserNotFoundException(f"User with id {user_id} does not exist")
        
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
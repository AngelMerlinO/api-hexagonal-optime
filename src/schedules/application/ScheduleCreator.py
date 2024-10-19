from src.schedules.domain.ScheduleRepository import ScheduleRepository
from src.users.domain.exceptions import UserNotFoundException
from src.schedules.domain.Schedule import Schedule
from src.schedules.domain.ScheduleItem import ScheduleItem
from typing import List, Dict
from src.users.domain.UserRepository import UserRepository
import uuid

class ScheduleCreator:
    def __init__(self, schedule_repository: ScheduleRepository, user_repository: UserRepository):
        self.schedule_repository = schedule_repository
        self.user_repository = user_repository

    def create(self, user_id: int, items: List[Dict]):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} does not exist")
        
        schedule_uuid = str(uuid.uuid4())
        
        new_schedule = Schedule(user_id=user.id, uuid=schedule_uuid)
        
        for item_data in items:
            schedule_item = ScheduleItem(
                nombre=item_data.get('nombre'),
                grupo=item_data.get('grupo'),
                cuatrimestre=item_data.get('cuatrimestre'),
                calif_cuatrimestre=item_data.get('calif_cuatrimestre'),
                calif_holgura=item_data.get('calif_holgura'),
                calif_seriacion=item_data.get('calif_seriacion'),
                lunes=item_data.get('lunes'),
                martes=item_data.get('martes'),
                miercoles=item_data.get('miercoles'),
                jueves=item_data.get('jueves'),
                viernes=item_data.get('viernes')
            )
            new_schedule.schedule_items.append(schedule_item)
            
        self.schedule_repository.save(new_schedule)
        return new_schedule
from src.schedules.domain.ScheduleRepository import ScheduleRepository
from src.users.domain.UserRepository import UserRepository
from src.schedules.domain.exceptions import ScheduleNotFoundException
from src.users.domain.exceptions import UserNotFoundException
from src.schedules.domain.ScheduleItem import ScheduleItem
from typing import List, Dict

class ScheduleUpdater:
    def __init__(self, schedule_repository: ScheduleRepository, user_repository: UserRepository):
        self.schedule_repository = schedule_repository
        self.user_repository = user_repository

    def update(self, schedule_id: int, user_id: int, items: List[Dict]):
        # Verificar si el usuario existe
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} does not exist")

        # Verificar si el schedule existe y pertenece al usuario
        schedule = self.schedule_repository.find_by_id(schedule_id)
        if not schedule:
            raise ScheduleNotFoundException(f"Schedule with id {schedule_id} does not exist")

        if schedule.user_id != user_id:
            raise PermissionError("User does not have permission to update this schedule")

        # Limpiar los items existentes
        schedule.schedule_items.clear()

        # Agregar los nuevos items
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
            schedule.schedule_items.append(schedule_item)

        self.schedule_repository.update(schedule)
        return schedule
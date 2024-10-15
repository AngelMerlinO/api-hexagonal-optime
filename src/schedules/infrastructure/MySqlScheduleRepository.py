from sqlalchemy.orm import Session
from typing import List
from src.schedules.domain.ScheduleRepository import ScheduleRepository
from src.schedules.domain.Schedule import Schedule
from src.schedules.infrastructure.orm.ScheduleModel import ScheduleModel
from src.schedules.infrastructure.orm.ScheduleItemModel import ScheduleItemModel
from src.schedules.domain.ScheduleItem import ScheduleItem

import uuid

class MySqlScheduleRepository(ScheduleRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, schedule: Schedule):
        schedule_uuid = schedule.uuid or str(uuid.uuid4()) 

        schedule_model = ScheduleModel(
            user_id=schedule.user_id,
            uuid=schedule_uuid
        )
        
        self.db_session.add(schedule_model)
        self.db_session.commit()
        self.db_session.refresh(schedule_model)
        
        for item in schedule.schedule_items:
            schedule_item_model = ScheduleItemModel(
                schedule_id=schedule_model.id,
                nombre=item.nombre,
                grupo=item.grupo,
                cuatrimestre=item.cuatrimestre,
                calif_cuatrimestre=item.calif_cuatrimestre,
                calif_holgura=item.calif_holgura,
                calif_seriacion=item.calif_seriacion,
                lunes=item.lunes,
                martes=item.martes,
                miercoles=item.miercoles,
                jueves=item.jueves,
                viernes=item.viernes
            )
            self.db_session.add(schedule_item_model)

        self.db_session.commit()
        self.db_session.refresh(schedule_model)
        
        schedule.id = schedule_model.id
        
        return schedule_model
    
    def find_by_uuid(self, uuid: str) -> Schedule:
        schedule_model = self.db_session.query(ScheduleModel).filter(ScheduleModel.uuid == uuid).first()
        if not schedule_model:
            raise ValueError(f"Schedule with UUID {uuid} not found")
        return self._to_domain(schedule_model)

    def find_by_user_id(self, user_id: int, skip: int = 0, limit: int = 3) -> List[Schedule]:
        schedules = self.db_session.query(ScheduleModel).filter_by(user_id=user_id).offset(skip).limit(limit).all()
        if not schedules:
            raise ValueError(f"No schedules found for user_id {user_id}")
        
        return [self._to_domain(schedule) for schedule in schedules]

    def find_by_id(self, schedule_id: int) -> Schedule:
        schedule_model = self.db_session.query(ScheduleModel).filter_by(id=schedule_id).first()
        if not schedule_model:
            raise ValueError(f"Schedule with ID {schedule_id} not found")
        return self._to_domain(schedule_model)


    def delete(self, schedule_id: int):
        try:
            schedule_model = self.db_session.query(ScheduleModel).filter_by(id=schedule_id).first()
            if not schedule_model:
                raise ValueError(f"Schedule with ID {schedule_id} not found")

            self.db_session.delete(schedule_model)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise ValueError(f"Error deleting schedule: {str(e)}")


    def update(self, schedule: Schedule):
        schedule_model = self.db_session.query(ScheduleModel).filter_by(id=schedule.id).first()
        if not schedule_model:
            raise ValueError(f"Schedule with ID {schedule.id} not found")
        
        schedule_model.user_id = schedule.user_id

        for item in schedule.schedule_items:
            schedule_item_model = self.db_session.query(ScheduleItemModel).filter_by(id=item.id).first()
            if schedule_item_model:
                schedule_item_model.nombre = item.nombre
                schedule_item_model.grupo = item.grupo
                schedule_item_model.cuatrimestre = item.cuatrimestre
                schedule_item_model.calif_cuatrimestre = item.calif_cuatrimestre
                schedule_item_model.calif_holgura = item.calif_holgura
                schedule_item_model.calif_seriacion = item.calif_seriacion
                schedule_item_model.lunes = item.lunes
                schedule_item_model.martes = item.martes
                schedule_item_model.miercoles = item.miercoles
                schedule_item_model.jueves = item.jueves
                schedule_item_model.viernes = item.viernes
            else:
                new_item_model = ScheduleItemModel(
                    schedule_id=schedule_model.id,
                    nombre=item.nombre,
                    grupo=item.grupo,
                    cuatrimestre=item.cuatrimestre,
                    calif_cuatrimestre=item.calif_cuatrimestre,
                    calif_holgura=item.calif_holgura,
                    calif_seriacion=item.calif_seriacion,
                    lunes=item.lunes,
                    martes=item.martes,
                    miercoles=item.miercoles,
                    jueves=item.jueves,
                    viernes=item.viernes
                )
                self.db_session.add(new_item_model)

        self.db_session.commit()
        self.db_session.refresh(schedule_model)
        return schedule_model

    def _to_domain(self, schedule_model: ScheduleModel) -> Schedule:
        schedule = Schedule(
            user_id=schedule_model.user_id,
            id=schedule_model.id,
            uuid=schedule_model.uuid
        )

        for item_model in schedule_model.schedule_items:
            schedule_item = ScheduleItem(
                nombre=item_model.nombre,
                grupo=item_model.grupo,
                cuatrimestre=item_model.cuatrimestre,
                calif_cuatrimestre=item_model.calif_cuatrimestre,
                calif_holgura=item_model.calif_holgura,
                calif_seriacion=item_model.calif_seriacion,
                lunes=item_model.lunes,
                martes=item_model.martes,
                miercoles=item_model.miercoles,
                jueves=item_model.jueves,
                viernes=item_model.viernes
            )
            schedule.schedule_items.append(schedule_item)

        return schedule

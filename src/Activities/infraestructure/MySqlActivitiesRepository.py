from typing import List
from src.Activities.domain.ActivitiesRepository import ActivitiesRepository
from src.Activities.domain.Activities import Activities, ActivityType, ActivityStatus
from src.Activities.infraestructure.orm.ActivitiesModel import ActivitiesModel, ActivityTypeEnum, ActivityStatusEnum
from sqlalchemy.orm import Session

class MySqlActivitiesRepository(ActivitiesRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def save(self, activity: ActivitiesModel):
        self.db_session.add(activity)
        self.db_session.commit()
        self.db_session.refresh(activity)
        return activity  # Ahora estamos devolviendo el modelo de infraestructura
    def update(self, activity: Activities):
        # Buscar el modelo de infraestructura y actualizar sus valores
        activity_model = self.db_session.query(ActivitiesModel).filter_by(id=activity.id).first()
        if not activity_model:
            raise ValueError(f"Activity with ID {activity.id} not found")
        
        # Actualizar el modelo de infraestructura con los valores del dominio
        activity_model.title = activity.title
        activity_model.description = activity.description
        activity_model.type = ActivityTypeEnum[activity.type.name]
        activity_model.status = ActivityStatusEnum[activity.status.name]
        activity_model.delivery_date = activity.delivery_date
        activity_model.link_classroom = activity.link_classroom

        self.db_session.merge(activity_model)
        self.db_session.commit()
        
    def find_by_id(self, activity_id: int) -> Activities:
        # Buscar el modelo de infraestructura
        activity_model = self.db_session.query(ActivitiesModel).filter_by(id=activity_id).first()
        if not activity_model:
            raise ValueError(f"Activity with ID {activity_id} not found")
        
        # Convertir el modelo de infraestructura a un objeto de dominio
        return Activities(
            id=activity_model.id,
            user_id=activity_model.user_id,
            title=activity_model.title,
            description=activity_model.description,
            activity_type=ActivityType[activity_model.type.name],  # Convertir 'type' a 'activity_type' en el dominio
            status=ActivityStatus[activity_model.status.name],
            delivery_date=activity_model.delivery_date,
            link_classroom=activity_model.link_classroom
        )
    
    
    def find_by_user_id(self, user_id: int) -> List[Activities]:
        # Buscar los modelos de infraestructura
        activities_models = self.db_session.query(ActivitiesModel).filter_by(user_id=user_id).all()
        
        # Convertir los modelos de infraestructura a objetos de dominio
        return [
            Activities(
                id=activity_model.id,
                user_id=activity_model.user_id,
                title=activity_model.title,
                description=activity_model.description,
                type=ActivityType[activity_model.type.name],
                status=ActivityStatus[activity_model.status.name],
                delivery_date=activity_model.delivery_date,
                link_classroom=activity_model.link_classroom
            )
            for activity_model in activities_models
        ]
    
    def delete(self, activity: Activities):
        # Buscar el modelo de infraestructura
        activity_model = self.db_session.query(ActivitiesModel).filter_by(id=activity.id).first()
        if not activity_model:
            raise ValueError(f"Activity with ID {activity.id} not found")
        
        self.db_session.delete(activity_model)
        self.db_session.commit()
        return f"Activities with ID {activity.id} eliminated successfully."
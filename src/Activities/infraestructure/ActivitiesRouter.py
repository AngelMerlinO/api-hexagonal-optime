from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.Activities.application.ActivitiesCreator import ActivitiesCreator
from src.Activities.application.ActivitiesFindById import ActivitiesFindByID
from src.Activities.application.ActivitiesUpdater import ActivitiesUpdater
from src.Activities.application.ActivitiesEliminator import ActivitiesEliminator
from src.Activities.infraestructure.MySqlActivitiesRepository import MySqlActivitiesRepository
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from config.database import get_db
from pydantic import BaseModel
from datetime import date
from fastapi import Query


from src.users.domain.exceptions import UserNotFoundException
from src.notifications.domain.exceptions import InvalidNotificationTypeException

router = APIRouter(
    prefix="/api/act/v1",
    tags=["activities"]
)

class ActivitiesCreate(BaseModel):
    title: str
    description: str
    delivery_date: date
    link_classroom: str
    type: str
    user_id: int
    status: str
    
    
class ActivitiesUpdate(BaseModel):
    title: str = None
    description: str = None
    delivery_date: date = None
    link_classroom: str = None
    type: str = None
    status: str = None
    
@router.get("/{activities_id}")
def find_by_id(activities_id: int, db: Session = Depends(get_db)):
    repo = MySqlActivitiesRepository(db)
    activities_finder = ActivitiesFindByID(repo)
    try:
        activities = activities_finder.find_by_id(activities_id)
        if not activities:
            raise HTTPException(status_code=404, detail=f"Activity with ID {activities_id} not found")
        
        # Devolvemos el objeto completo utilizando el modelo Pydantic
        return activities
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error finding activities: {str(e)}")

    
@router.post("/")
def create_activities(
    activity_data: ActivitiesCreate,
    db: Session = Depends(get_db)
):
    activity_repo = MySqlActivitiesRepository(db)
    user_repo = MySqlUserRepository(db)
    activities_creator = ActivitiesCreator(activity_repo, user_repo)
    try:
        activity = activities_creator.create(
        activity_data.title, 
        activity_data.description, 
        activity_data.delivery_date, 
        activity_data.link_classroom, 
        activity_data.user_id,  
        activity_data.type, 
        activity_data.status  
    )
        db.commit() 
        db.refresh(activity)  
        return {"message": "Activity created successfully", "Activity_id": activity.id}
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidNotificationTypeException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{activities_id}")
def update_activities(activities_id: int, activities: ActivitiesUpdate, db: Session = Depends(get_db)):
    repo = MySqlActivitiesRepository(db)
    activities_updater = ActivitiesUpdater(repo)
    try:
        # Primero se busca la actividad existente
        existing_activity = repo.find_by_id(activities_id)
        if not existing_activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        # Actualiza los campos que no sean None
        if activities.title is not None:
            existing_activity.title = activities.title
        if activities.description is not None:
            existing_activity.description = activities.description
        if activities.delivery_date is not None:
            existing_activity.delivery_date = activities.delivery_date
        if activities.link_classroom is not None:
            existing_activity.link_classroom = activities.link_classroom
        if activities.type is not None:
            existing_activity.type = activities.type
        if activities.status is not None:
            existing_activity.status = activities.status

        # Guardar los cambios
        repo.update(existing_activity)

        return {"message": "Activities updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/")
def delete_activities(
    activities_id = Query(..., description="ID of the activity to be deleted"), 
    db: Session = Depends(get_db)
    ):
    repo = MySqlActivitiesRepository(db)
    activities_eliminator = ActivitiesEliminator(repo) 
    try:
        # Llama al eliminador para eliminar la actividad
        activities_eliminator.delete(activities_id)
        return {"message": f"Activities with ID {activities_id} eliminated successfully"}
    except ValueError as e:
        # Captura el error y devuelve una excepción HTTP 404
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Captura cualquier otro error y devuelve un HTTP 400
        raise HTTPException(status_code=400, detail=str(e))



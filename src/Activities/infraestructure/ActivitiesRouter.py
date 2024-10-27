from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.Activities.application.ActivitiesCreator import ActivitiesCreator
from src.Activities.application.ActivitiesFindById import ActivitiesFindByID
from src.Activities.application.ActivitiesUpdater import ActivitiesUpdater
from src.Activities.application.ActivitiesEliminator import ActivitiesEliminator
from src.Activities.infraestructure.MySqlActivitiesRepository import MySqlActivitiesRepository
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from slowapi import Limiter
from slowapi.util import get_remote_address
from config.database import get_db
from pydantic import BaseModel
from datetime import date
from fastapi import Query

from src.users.domain.exceptions import UserNotFoundException
from src.notifications.domain.exceptions import InvalidNotificationTypeException
from src.Activities.domain.exceptions import InvalidActivityTypeException, InvalidActivityStatusException

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/api/v1/act",
    tags=["activities"]
)

class ActivitiesCreate(BaseModel):
    title: str
    description: str
    delivery_date: date
    link_classroom: str
    activity_type: str  
    user_id: int
    status: str

class ActivitiesUpdate(BaseModel):
    title: str = None
    description: str = None
    delivery_date: date = None
    link_classroom: str = None
    activity_type: str = None 
    status: str = None
    
@router.get("/{activities_id}")
@limiter.limit("2/minute")  
def find_by_id(activities_id: int, request:Request, db: Session = Depends(get_db)):
    activity_repo = MySqlActivitiesRepository(db)
    
    try:
        activity_model = activity_repo.find_by_id(activities_id)
        if not activity_model:
            raise HTTPException(status_code=404, detail=f"Activity with ID {activities_id} not found")
        
        return {
            "id": activity_model.id,
            "uuid": activity_model.uuid,
            "user_id": activity_model.user_id,
            "title": activity_model.title,
            "description": activity_model.description,
            "activity_type": activity_model.type.name,  
            "status": activity_model.status.name, 
            "delivery_date": activity_model.delivery_date,
            "link_classroom": activity_model.link_classroom
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error finding activities: {str(e)}")
    
@router.post("/")
@limiter.limit("2/minute")  
def create_activities(
    activity_data: ActivitiesCreate,
    request: Request,
    db: Session = Depends(get_db) 
):
    activity_repo = MySqlActivitiesRepository(db)
    user_repo = MySqlUserRepository(db)

    activities_creator = ActivitiesCreator(activity_repo, user_repo)
    
    try:
        activity_model = activities_creator.create(
            activity_data.title, 
            activity_data.description, 
            activity_data.delivery_date, 
            activity_data.link_classroom, 
            activity_data.user_id,  
            activity_data.activity_type, 
            activity_data.status
        )
        
        db.commit()
        db.refresh(activity_model)

        return {"message": "Activity created successfully", "activity_id": activity_model.id}
    
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except InvalidActivityTypeException as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except InvalidActivityStatusException as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{activities_id}")
@limiter.limit("2/minute")  
def update_activities(activities_id: int, request:Request, activities: ActivitiesUpdate, db: Session = Depends(get_db)):
    repo = MySqlActivitiesRepository(db)
    activities_updater = ActivitiesUpdater(repo)
    try:
        existing_activity = repo.find_by_id(activities_id)
        if not existing_activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        
        if activities.title is not None:
            existing_activity.title = activities.title
        if activities.description is not None:
            existing_activity.description = activities.description
        if activities.delivery_date is not None:
            existing_activity.delivery_date = activities.delivery_date
        if activities.link_classroom is not None:
            existing_activity.link_classroom = activities.link_classroom
        if activities.activity_type is not None: 
            existing_activity.type = activities.activity_type
        if activities.status is not None:
            existing_activity.status = activities.status

        repo.update(existing_activity)

        return {"message": "Activities updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/")
@limiter.limit("2/minute")  
def delete_activities(
    request: Request,
    activities_id = Query(..., description="ID of the activity to be deleted"), 
    db: Session = Depends(get_db),
    ):
    repo = MySqlActivitiesRepository(db)
    activities_eliminator = ActivitiesEliminator(repo) 
    try:
        activities_eliminator.delete(activities_id)
        return {"message": f"Activities with ID {activities_id} eliminated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



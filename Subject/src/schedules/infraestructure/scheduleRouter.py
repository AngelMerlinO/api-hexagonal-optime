from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from src.schedules.infraestructure.MySqlScheduleRepository import MySqlScheduleRepository
from src.schedules.application.useCases.scheduleFindById import SchedulesFindById
from src.schedules.application.useCases.scheduleCreator import SchedulesCreator
from src.schedules.application.useCases.scheduleEliminator import SchedulesEliminator
from src.schedules.application.useCases.scheduleUpdate import SchedulesUpdater
from src.subject.infraestructure.orm.subjectModels import SubjectModel
from src.schedules.domain.schedule import Schedule
from src.subject.domain.subject import Subject
from config.database import get_db
from src.auth.jwt_handler import get_current_user
from slowapi.util import get_remote_address
from slowapi import Limiter
from pydantic import BaseModel
from typing import List


limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/api/v1/schedules",
    tags=["schedules"]
)

class SubjectCreate(BaseModel):
    name: str
    period: int
    group: str
    semester_grade: int
    serialization_raiting: int
    clearance_raiting: int
    monday: List[int]
    tuesday: List[int]
    wednesday: List[int]
    thursday: List[int]
    friday: List[int]

class ScheduleCreate(BaseModel):
    user_id: int
    items: List[SubjectCreate]
    
class ScheduleUpdate(BaseModel):
    items: List[SubjectCreate] = None
    

@router.get("/{schedule_id}")
@limiter.limit("2/minute")
def find_by_id(
    schedule_id: int,
    request: Request, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    schedule_repo = MySqlScheduleRepository(db)
    finder = SchedulesFindById(schedule_repo)
    
    try:
        schedule = finder.find_by_id(schedule_id)
        if not schedule:
            raise HTTPException(status_code=404, detail=f"Schedule with ID {schedule_id} not found")
        return {
            "id": schedule.id,
            "uuid": schedule.uuid,
            "user_id": schedule.user_id,
            "subjects": [
                {
                    "id": s.id, 
                    "name": s.name, 
                    "group": s.group,
                    "monday": s.monday,
                    "tuesday": s.tuesday,
                    "wednesday": s.wednesday,
                    "thursday": s.thursday,
                    "friday": s.friday,
                    } 
                for s in schedule.subjects
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@router.post("/")
@limiter.limit("2/minute")
def create_schedule(
    schedule_data: ScheduleCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    schedule_repo = MySqlScheduleRepository(db)
    subjects = [
        Subject(**subject.dict()) for subject in schedule_data.items
    ]
    new_schedule = Schedule(user_id=schedule_data.user_id, items=subjects)
    
    creator = SchedulesCreator(schedule_repo)
    try:
        created_schedule = creator.create(new_schedule)
        return {"message": "Schedule created successfully", "schedule_id": created_schedule.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@router.put("/{schedule_id}")
@limiter.limit("2/minute")
def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    schedule_repo = MySqlScheduleRepository(db)
    updater = SchedulesUpdater(schedule_repo)
    
    try:
        updated_schedule = updater.update(schedule_id, schedule_data.dict(exclude_unset=True))
        return {"message": "Schedule updated successfully", "schedule": updated_schedule}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/")
@limiter.limit("2/minute")
def delete_schedule(
    request: Request,
    schedule_id: int = Query(..., description="ID of the schedule to be deleted"),
    db: Session = Depends(get_db),
    # current_user: str = Depends(get_current_user)
):
    schedule_repo = MySqlScheduleRepository(db)
    eliminator = SchedulesEliminator(schedule_repo)
    try:
        eliminator.delete(schedule_id)
        return {"message": f"Schedule with ID {schedule_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
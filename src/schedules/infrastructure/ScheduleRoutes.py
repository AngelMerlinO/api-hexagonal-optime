from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from src.schedules.application.ScheduleCreator import ScheduleCreator
from src.schedules.application.ScheduleDeleter import ScheduleDeleter
from src.schedules.application.ScheduleUpdater import ScheduleUpdater
from src.schedules.application.ScheduleRetriever import ScheduleRetriever
from src.schedules.infrastructure.MySqlScheduleRepository import MySqlScheduleRepository
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from src.users.domain.exceptions import UserNotFoundException
from src.schedules.domain.exceptions import ScheduleNotFoundException
from src.auth.jwt_handler import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address
from config.database import get_db
from pydantic import BaseModel
from typing import List, Optional

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix=("/api/v1/schedules"),
    tags=["schedules"]
)

class ScheduleItemModel(BaseModel):
    nombre: str
    grupo: Optional[str] = None
    cuatrimestre: Optional[int] = None
    calif_cuatrimestre: Optional[int] = None
    calif_holgura: Optional[int] = None
    calif_seriacion: Optional[int] = None
    lunes: List[int] = []
    martes: List[int] = []
    miercoles: List[int] = []
    jueves: List[int] = []
    viernes: List[int] = []

class ScheduleCreateModel(BaseModel):
    user_id: int
    items: List[ScheduleItemModel]

class ScheduleUpdateModel(BaseModel):
    user_id: int
    items: List[ScheduleItemModel]

@router.post("/")
@limiter.limit("2/minute")  
def create_schedule(
    schedule_data: ScheduleCreateModel,
    request:Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    schedule_repo = MySqlScheduleRepository(db)
    user_repo = MySqlUserRepository(db)
    schedule_creator = ScheduleCreator(schedule_repo, user_repo)
    try:
        schedule = schedule_creator.create(
            schedule_data.user_id,
            [item.dict() for item in schedule_data.items]
        )
        return {"message": "Schedule created successfully", "schedule_id": schedule.id}
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{schedule_id}")
@limiter.limit("2/minute")  
def delete_schedule(
    schedule_id: int,
    request:Request,
    user_id: int = Query(..., description="User ID is required"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    repo = MySqlScheduleRepository(db)
    try:
        repo.delete(schedule_id)
        return {"message": f"Schedule with ID {schedule_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{schedule_uuid}")
@limiter.limit("2/minute")  
def update_schedule(
    schedule_uuid: str,  
    schedule_data: ScheduleUpdateModel,
    request:Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    schedule_repo = MySqlScheduleRepository(db)
    user_repo = MySqlUserRepository(db)
    schedule_updater = ScheduleUpdater(schedule_repo, user_repo)

    try:
        schedule = schedule_updater.update(
            schedule_uuid,
            schedule_data.user_id,
            [item.dict() for item in schedule_data.items]
        )
        return {"message": "Schedule updated successfully", "schedule_id": schedule.id}
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ScheduleNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{schedule_id}/class/{schedule_uuid}")
def get_schedules(
    user_id: int = Query(..., description="User ID is required"),
    skip: int = Query(0, ge=0, description="Number of elements to skip"),
    limit: int = Query(6, ge=1, le=100, description="Maximum number of items to return"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    schedule_repo = MySqlScheduleRepository(db)
    user_repo = MySqlUserRepository(db)
    schedule_retriever = ScheduleRetriever(schedule_repo, user_repo)
    try:
        schedules = schedule_retriever.get_by_user_id(user_id, skip=skip, limit=limit)
        schedules_data = []
        for schedule in schedules:
            schedule_data = {
                "id": schedule.id,
                "uuid": schedule.uuid,
                "user_id": schedule.user_id,
                "items": [
                    {
                        "nombre": item.nombre,
                        "grupo": item.grupo,
                        "cuatrimestre": item.cuatrimestre,
                        "calif_cuatrimestre": item.calif_cuatrimestre,
                        "calif_holgura": item.calif_holgura,
                        "calif_seriacion": item.calif_seriacion,
                        "lunes": item.lunes,
                        "martes": item.martes,
                        "miercoles": item.miercoles,
                        "jueves": item.jueves,
                        "viernes": item.viernes,
                    }
                    for item in schedule.schedule_items
                ]
            }
            schedules_data.append(schedule_data)
        return schedules_data
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ScheduleNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
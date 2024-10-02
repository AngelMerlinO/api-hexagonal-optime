# src/schedules/infrastructure/ScheduleRoutes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schedules.application.ScheduleCreator import ScheduleCreator
from src.schedules.application.ScheduleDeleter import ScheduleDeleter
from src.schedules.infrastructure.MySqlScheduleRepository import MySqlScheduleRepository
from config.database import get_db
from pydantic import BaseModel
from typing import List, Optional

from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from src.users.domain.exceptions import UserNotFoundException
from src.schedules.domain.exceptions import ScheduleNotFoundException

router = APIRouter()

# Modelos Pydantic
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

@router.post("/schedules/")
def create_schedule(
    schedule_data: ScheduleCreateModel,
    db: Session = Depends(get_db)
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

@router.delete("/schedules/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    schedule_repo = MySqlScheduleRepository(db)
    user_repo = MySqlUserRepository(db)
    schedule_deleter = ScheduleDeleter(schedule_repo, user_repo)
    try:
        schedule_deleter.delete(schedule_id, user_id)
        return {"message": "Schedule deleted successfully"}
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ScheduleNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
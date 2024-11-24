from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from src.subject.infraestructure.MySqlSubjectRepository import MySqlSubjectRepository
from config.database import get_db
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/api/v1/subjects",
    tags=["subjects"]
)

class SubjectCreate(BaseModel):
    schedule_id: int
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

class SubjectUpdate(BaseModel):
    name: str = None
    period: int = None
    group: str = None
    semester_grade: int = None
    serialization_raiting: int = None
    clearance_raiting: int = None
    monday: List[int] = None
    tuesday: List[int] = None
    wednesday: List[int] = None
    thursday: List[int] = None
    friday: List[int] = None


@router.post("/")
def create_subject(
    subject_data: SubjectCreate,
    db: Session = Depends(get_db)
):
    subject_repo = MySqlSubjectRepository(db)
    try:
        new_subject = subject_repo.create(subject_data.dict())
        return {"message": "Subject created successfully", "subject_id": new_subject.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{subject_id}")
def find_subject_by_id(
    subject_id: int,
    db: Session = Depends(get_db)
):
    subject_repo = MySqlSubjectRepository(db)
    subject = subject_repo.find_by_id(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject with ID {subject_id} not found")
    return {
        "id": subject.id,
        "schedule_id": subject.schedule_id,
        "name": subject.name,
        "period": subject.period,
        "group": subject.group,
        "semester_grade": subject.semester_grade,
        "serialization_raiting": subject.serialization_raiting,
        "clearance_raiting": subject.clearance_raiting,
        "monday": subject.monday,
        "tuesday": subject.tuesday,
        "wednesday": subject.wednesday,
        "thursday": subject.thursday,
        "friday": subject.friday
    }


@router.get("/schedule/{schedule_id}")
def list_subjects_by_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    subject_repo = MySqlSubjectRepository(db)
    subjects = subject_repo.find_all(schedule_id)
    if not subjects:
        raise HTTPException(status_code=404, detail=f"No subjects found for Schedule ID {schedule_id}")
    return [{"id": s.id, "name": s.name, "group": s.group, "period": s.period} for s in subjects]


@router.put("/{subject_id}")
def update_subject(
    subject_id: int,
    subject_data: SubjectUpdate,
    db: Session = Depends(get_db)
):
    subject_repo = MySqlSubjectRepository(db)
    try:
        updated_subject = subject_repo.update(subject_id, subject_data.dict(exclude_unset=True))
        return {"message": "Subject updated successfully", "subject_id": updated_subject.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db)
):
    subject_repo = MySqlSubjectRepository(db)
    try:
        subject_repo.delete(subject_id)
        return {"message": f"Subject with ID {subject_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

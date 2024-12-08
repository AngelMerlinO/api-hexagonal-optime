from sqlalchemy.orm import Session
from src.schedules.domain.scheduleRepository import ScheduleRepository
from src.schedules.domain.schedule import Schedule
from src.schedules.infraestructure.orm.scheduleModel import SchedulesModel
from src.subject.infraestructure.orm.subjectModels import SubjectModel
import uuid

class MySqlScheduleRepository(SchedulesModel):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def save(self, schedule: Schedule):
        new_schedule = SchedulesModel(
            user_id=schedule.user_id,
            uuid=schedule.uuid or str(uuid.uuid4())
        )

        self.db_session.add(new_schedule)
        self.db_session.commit() 

        for subject_data in schedule.items:
            new_subject = SubjectModel(
                schedule_id=new_schedule.id,
                name=subject_data.name,
                period=subject_data.period,
                group=subject_data.group,
                semester_grade=subject_data.semester_grade,
                serialization_raiting=subject_data.serialization_raiting,
                clearance_raiting=subject_data.clearance_raiting,
                monday=subject_data.monday,
                tuesday=subject_data.tuesday,
                wednesday=subject_data.wednesday,
                thursday=subject_data.thursday,
                friday=subject_data.friday
            )
            self.db_session.add(new_subject)

        self.db_session.commit()
        return new_schedule
    
    def update(self, schedule_id: int, updated_data: dict) -> SchedulesModel:
        schedule = self.find_by_id(schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found.")

        existing_subjects = {subject.id: subject for subject in schedule.subjects}

        new_subjects = []
        for subject_data in updated_data.get("items", []):
            subject_id = subject_data.get("id")
            if subject_id and subject_id in existing_subjects:
                subject = existing_subjects[subject_id]
                for key, value in subject_data.items():
                    if hasattr(subject, key) and value is not None:
                        setattr(subject, key, value)
            else:
                new_subject = SubjectModel(
                    schedule_id=schedule.id,
                    name=subject_data["name"],
                    period=subject_data["period"],
                    group=subject_data["group"],
                    semester_grade=subject_data["semester_grade"],
                    serialization_raiting=subject_data["serialization_raiting"],
                    clearance_raiting=subject_data["clearance_raiting"],
                    monday=subject_data["monday"],
                    tuesday=subject_data["tuesday"],
                    wednesday=subject_data["wednesday"],
                    thursday=subject_data["thursday"],
                    friday=subject_data["friday"],
                )
                new_subjects.append(new_subject)

        updated_subject_ids = [s["id"] for s in updated_data.get("items", []) if "id" in s]
        for subject_id in list(existing_subjects.keys()):
            if subject_id not in updated_subject_ids:
                self.db_session.delete(existing_subjects[subject_id])

        schedule.subjects.extend(new_subjects)

        self.db_session.add(schedule)
        self.db_session.commit()
        self.db_session.refresh(schedule)

        return schedule
        
    
    def find_by_id(self, schedule_id: int) -> SchedulesModel:
        return self.db_session.query(SchedulesModel).filter_by(id=schedule_id).first()
    
    def delete(self, schedule_id: int):
        schedule = self.find_by_id(schedule_id)
        if schedule:
            self.db_session.delete(schedule)
            self.db_session.commit()
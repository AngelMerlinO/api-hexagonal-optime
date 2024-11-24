from sqlalchemy.orm import Session
from src.subject.domain.subjectRepository import SubjectRepository
from src.subject.domain.subject import Subject
from src.subject.infraestructure.orm.subjectModels import SubjectModel

class MySqlSubjectRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_by_id(self, subject_id: int) -> SubjectModel:
        return self.db_session.query(SubjectModel).filter_by(id=subject_id).first()

    def create(self, subject: SubjectModel) -> SubjectModel:
        self.db_session.add(subject)
        self.db_session.commit()
        self.db_session.refresh(subject)
        return subject

    def update(self, subject_id: int, updated_data: dict) -> SubjectModel:
        subject = self.find_by_id(subject_id)
        if not subject:
            raise ValueError(f"Subject with ID {subject_id} not found")

        for key, value in updated_data.items():
            if hasattr(subject, key) and value is not None:
                setattr(subject, key, value)

        self.db_session.commit()
        self.db_session.refresh(subject)
        return subject

    def delete(self, subject_id: int) -> None:
        subject = self.find_by_id(subject_id)
        if not subject:
            raise ValueError(f"Subject with ID {subject_id} not found")

        self.db_session.delete(subject)
        self.db_session.commit()

    def find_all(self, schedule_id: int) -> list[SubjectModel]:
        return self.db_session.query(SubjectModel).filter_by(schedule_id=schedule_id).all()
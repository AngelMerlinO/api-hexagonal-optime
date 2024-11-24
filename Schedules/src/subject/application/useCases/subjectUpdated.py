from sqlalchemy.orm import Session
from src.subject.domain.subject import Subject
from src.subject.domain.subjectRepository import SubjectRepository

class SubjectUpdater:
    def __init__(self, subject_repo: SubjectRepository):
        self.subject_repo = subject_repo

    def update(self, subject_id: int, updated_data: dict) -> Subject:
        subject = self.subject_repo.find_by_id(subject_id)
        if not subject:
            raise ValueError(f"Subject with ID {subject_id} not found.")
        
        for key, value in updated_data.items():
            if hasattr(subject, key) and value is not None:
                setattr(subject, key, value)

        self.subject_repo.update(subject)

        return subject

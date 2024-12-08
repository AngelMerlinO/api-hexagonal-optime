from src.subject.domain.subjectRepository import SubjectRepository

class SubjectFindById:
    def __init__(self, subject_repo: SubjectRepository):
        self.subject_repo = subject_repo
        
    def find_by_id(self, subject_id: int):
        subject = self.subject_repo.find_by_id(subject_id)
        if not subject:
            raise ValueError(f"Subject with ID {subject_id} does not exist.")
        
        return subject
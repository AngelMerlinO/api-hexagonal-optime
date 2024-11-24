from src.subject.domain.subjectRepository import SubjectRepository
from src.subject.domain.subject import Subject
from src.subject.infraestructure.orm.subjectModels import SubjectModel

class SubjectCreator:
    def __init__(self, subject_repo: SubjectRepository):
        self.subject_repo = subject_repo
        
    def create(self, subject: Subject) -> Subject:
        created_subject = self.subject_repo.save(subject)
        
        return created_subject
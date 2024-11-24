from abc import ABC, abstractmethod
from typing import List
from src.subject.domain.subject import Subject

class SubjectRepository(ABC):
    @abstractmethod
    def save(self, subject: Subject):
        pass
    
    @abstractmethod
    def find_by_id(self, subject_id: int) -> Subject:
        pass
    
    @abstractmethod
    def update(self, subject_id: int) -> Subject:
        pass
    
    @abstractmethod
    def delete(self, subject: Subject):
        pass    
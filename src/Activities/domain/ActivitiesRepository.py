from abc import ABC, abstractmethod
from typing import List
from src.Activities.domain.Activities import Activities

class ActivitiesRepository(ABC):
    @abstractmethod
    def save(self, activity: Activities):
        pass
    
    @abstractmethod
    def update(self, activity: Activities):
        pass
    
    @abstractmethod
    def find_by_id(self, activity_id: int) -> Activities:
        pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Activities]:
        pass
    
    @abstractmethod
    def delete(self, activity: Activities):
        pass
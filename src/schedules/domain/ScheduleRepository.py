from abc import ABC, abstractmethod
from typing import List
from .Schedule import Schedule

class ScheduleRepository(ABC):
    @abstractmethod
    def save(self, schedule: Schedule):
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Schedule]:
        pass

    @abstractmethod
    def find_by_id(self, schedule_id: int) -> Schedule:
        pass

    @abstractmethod
    def delete(self, schedule: Schedule):
        pass

    @abstractmethod
    def update(self, schedule: Schedule):
        pass
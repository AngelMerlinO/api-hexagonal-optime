# src/schedules/domain/ScheduleRepository.py
from abc import ABC, abstractmethod
from typing import List
from .Schedule import Schedule

class ScheduleRepository(ABC):
    @abstractmethod
    def save(self, schedule: Schedule):
        """Guarda un horario en el repositorio"""
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Schedule:
        """Encuentra un horario por el ID del usuario"""
        pass
    @abstractmethod
    def delete(self, schedule: Schedule):
        pass
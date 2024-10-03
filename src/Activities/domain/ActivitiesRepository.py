from abc import ABC, abstractmethod
from typing import List
from .Activities import Activities

class ActivitiesRepository(ABC):
    @abstractmethod
    def save(self, activities: Activities):
        """Guarda ua actividad en el repositorio"""
        pass
    
    @abstractmethod
    def update(self, activities: Activities):
        """Actualiza los datos de la actividad en el repositorio"""
        pass
    
    @abstractmethod
    def find_by_id(self, activities_id: int) -> Activities:
        """Encuentra una actividad por ID"""
        pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Activities]:
        pass
    
    @abstractmethod
    def delete(self, activities: Activities):
        """Elimina una actividad mediante el ID"""
        pass
    
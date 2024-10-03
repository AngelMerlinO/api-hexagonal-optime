from src.Activities.domain.ActivitiesRepository import ActivitiesRepository
from src.Activities.domain.Activities import Activities

class ActivitiesEliminator:
    def __init__(self, activities_repository: ActivitiesRepository):
        self.activities_repository = activities_repository
        
    def delete(self, activities_id: int):
        # Busca la actividad en el repositorio
        activity = self.activities_repository.find_by_id(activities_id)
        
        # Si no se encuentra, lanza una excepción
        if not activity:
            raise ValueError(f"Activities with ID {activities_id} not found.")
        
        # Si se encuentra, eliminar la actividad
        self.activities_repository.delete(activity)

from src.payments.domain.Timestamp import Timestamps

class TimestampService:
    def __init__(self, repository):
        """El servicio interactúa con un repositorio (ej: base de datos)"""
        self.repository = repository

    def create_with_timestamps(self, entity_data):
        """Crea una nueva entidad con timestamps por defecto."""
        timestamps = Timestamps()
        entity_data['timestamps'] = timestamps
        self.repository.save(entity_data)

    def mark_entity_as_deleted(self, entity_id):
        """Marca una entidad como eliminada."""
        entity = self.repository.find_by_id(entity_id)
        if entity:
            entity.timestamps.mark_deleted()
            self.repository.update(entity)

    def update_entity_timestamp(self, entity_id):
        """Actualiza el timestamp updated_at de una entidad."""
        entity = self.repository.find_by_id(entity_id)
        if entity:
            entity.timestamps.update_timestamp()
            self.repository.update(entity)
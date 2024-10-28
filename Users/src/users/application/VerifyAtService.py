from src.users.domain.VerifyAt import VerifyAt

class VerifyAtService:
    def __init__(self, repository):
        """El servicio interactúa con un repositorio (ej: base de datos)."""
        self.repository = repository

    def create_with_verify_at(self, entity_data):
        """Crea una nueva entidad con el campo de verificación."""
        verify_at = VerifyAt()
        entity_data['verify_at'] = verify_at
        self.repository.save(entity_data)

    def mark_entity_as_verified(self, entity_id):
        """Marca una entidad como verificada."""
        entity = self.repository.find_by_id(entity_id)
        if entity:
            entity.verify_at.mark_verified()
            self.repository.update(entity)

    def is_entity_verified(self, entity_id):
        """Verifica si una entidad ha sido marcada como verificada."""
        entity = self.repository.find_by_id(entity_id)
        if entity:
            return entity.verify_at.is_verified()
        return False

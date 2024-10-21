from datetime import datetime

class Timestamps:
    def __init__(self, created_at=None, updated_at=None, deleted_at=None):
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.deleted_at = deleted_at

    def mark_deleted(self):
        """Marca como eliminado actualizando el deleted_at."""
        self.deleted_at = datetime.utcnow()

    def update_timestamp(self):
        """Actualiza el campo updated_at con la hora actual."""
        self.updated_at = datetime.utcnow()

    def is_deleted(self):
        """Verifica si el objeto ha sido marcado como eliminado."""
        return self.deleted_at is not None

    def __eq__(self, other):
        if not isinstance(other, Timestamps):
            return False
        return (self.created_at == other.created_at and 
                self.updated_at == other.updated_at and 
                self.deleted_at == other.deleted_at)

    def __repr__(self):
        return f"<Timestamps(created_at={self.created_at}, updated_at={self.updated_at}, deleted_at={self.deleted_at})>"

from datetime import datetime

class VerifyAt:
    def __init__(self, verified_at=None):
        """Inicializa el objeto con una fecha de verificación opcional."""
        self.verified_at = verified_at

    def mark_verified(self):
        """Marca como verificado actualizando el verified_at."""
        self.verified_at = datetime.utcnow()

    def is_verified(self):
        """Verifica si el objeto ha sido marcado como verificado."""
        return self.verified_at is not None

    def __eq__(self, other):
        """Compara dos objetos VerifyAt por sus fechas de verificación."""
        if not isinstance(other, VerifyAt):
            return False
        return self.verified_at == other.verified_at

    def __repr__(self):
        return f"<VerifyAt(verified_at={self.verified_at})>"

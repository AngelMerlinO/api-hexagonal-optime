import sqlalchemy as sa
from sqlalchemy.types import TypeDecorator, DateTime
from datetime import datetime
from src.users.domain.VerifyAt import VerifyAt

class VerifyAtType(TypeDecorator):
    """Clase que permite almacenar el VerifyAt como DateTime en la base de datos."""
    impl = DateTime

    def process_bind_param(self, value, dialect):
        """Convierte el objeto VerifyAt en datetime para la base de datos"""
        if value is None:
            return None
        if isinstance(value, VerifyAt):
            return value.verified_at 
        raise ValueError("Se esperaba un objeto VerifyAt")

    def process_result_value(self, value, dialect):
        """Convierte el valor de la base de datos en un objeto VerifyAt"""
        if value is None:
            return VerifyAt(None)
        return VerifyAt(verified_at=value)  

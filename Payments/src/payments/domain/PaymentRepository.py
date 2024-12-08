# src/payments/domain/PaymentRepository.py
from abc import ABC, abstractmethod
from .Payment import Payment
from typing import Optional

class PaymentRepository(ABC):
    @abstractmethod
    def save(self, payment: Payment):
        """Guarda un nuevo pago en el repositorio."""
        pass

    @abstractmethod
    def update(self, payment: Payment):
        """Actualiza un pago existente en el repositorio."""
        pass

    @abstractmethod
    def find_by_id(self, payment_id: int) -> Optional[Payment]:
        """Busca un pago por su ID interno.
        
        Args:
            payment_id (int): El ID interno del pago.

        Returns:
            Optional[Payment]: El pago si es encontrado, de lo contrario None.
        """
        pass

    @abstractmethod
    def find_by_payment_id(self, payment_id: str) -> Optional[Payment]:
        """Busca un pago por su ID externo (ej. ID de Mercado Pago).
        
        Args:
            payment_id (str): El ID externo del pago.

        Returns:
            Optional[Payment]: El pago si es encontrado, de lo contrario None.
        """
        pass

    @abstractmethod
    def find_by_preference_id(self, preference_id: str) -> Optional[Payment]:
        """Busca un pago por su ID de preferencia.
        
        Args:
            preference_id (str): El ID de preferencia del pago.

        Returns:
            Optional[Payment]: El pago si es encontrado, de lo contrario None.
        """
        pass

    @abstractmethod
    def delete(self, payment: Payment):
        """Elimina un pago del repositorio.
        
        Args:
            payment (Payment): El objeto de pago a eliminar.
        """
        pass
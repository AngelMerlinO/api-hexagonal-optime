from abc import ABC, abstractmethod
from typing import List
from .Payment import Payment

class PaymentRepository(ABC):
    @abstractmethod
    def save(self, payment: Payment):
        pass

    @abstractmethod
    def update(self, payment: Payment):
        pass

    @abstractmethod
    def find_by_id(self, payment_id: int) -> Payment:
        pass

    @abstractmethod
    def find_by_payment_id(self, payment_id: str) -> Payment:
        pass

    @abstractmethod
    def find_by_preference_id(self, preference_id: str) -> Payment:
        pass
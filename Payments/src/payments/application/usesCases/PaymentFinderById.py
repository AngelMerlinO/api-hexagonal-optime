# Payments/src/payments/application/usesCases/PaymentFinderById.py

from src.payments.domain.PaymentRepository import PaymentRepository

class PaymentFinderById:
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    def find_by_id(self, payment_id: int):
        payment = self.payment_repository.find_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment with ID {payment_id} not found")
        return payment
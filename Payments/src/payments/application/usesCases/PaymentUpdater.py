# Payments/src/payments/application/usesCases/PaymentUpdater.py

from src.payments.domain.PaymentRepository import PaymentRepository

class PaymentUpdater:
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    def update(self, payment_id: int, **kwargs):
        payment = self.payment_repository.find_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment with ID {payment_id} not found")

        for key, value in kwargs.items():
            if hasattr(payment, key):
                setattr(payment, key, value)

        self.payment_repository.update(payment)
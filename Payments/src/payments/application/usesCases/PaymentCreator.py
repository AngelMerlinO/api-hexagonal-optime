# Payments/src/payments/application/usesCases/PaymentCreator.py

from src.payments.domain.PaymentRepository import PaymentRepository
from src.payments.domain.Payment import Payment

class PaymentCreator:
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    def create(self, user_id: int, preference_id: str, amount: float, currency_id: str, description: str = None) -> Payment:
        new_payment = Payment(
            user_id=user_id,
            preference_id=preference_id,
            amount=amount,
            currency_id=currency_id,
            description=description
        )
        self.payment_repository.save(new_payment)
        return new_payment
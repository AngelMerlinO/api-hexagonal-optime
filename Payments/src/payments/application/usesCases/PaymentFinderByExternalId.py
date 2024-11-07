# Payments/src/payments/application/usesCases/PaymentFinderByExternalId.py

from src.payments.domain.PaymentRepository import PaymentRepository

class PaymentFinderByExternalId:
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    def find_by_external_id(self, external_id: str):
        payment = self.payment_repository.find_by_external_id(external_id)
        if not payment:
            raise ValueError(f"Payment with external ID {external_id} not found")
        return payment
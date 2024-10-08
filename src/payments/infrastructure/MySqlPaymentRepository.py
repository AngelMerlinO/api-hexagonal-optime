from src.payments.domain.PaymentRepository import PaymentRepository
from src.payments.infrastructure.orm.PaymentModel import PaymentModel
from sqlalchemy.orm import Session
from typing import List

class MySqlPaymentRepository(PaymentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, payment: PaymentModel):
        self.db_session.add(payment)
        self.db_session.commit()
        self.db_session.refresh(payment)
        return payment

    def update(self, payment: PaymentModel):
        self.db_session.commit()
        self.db_session.refresh(payment)
        return payment

    def find_by_id(self, payment_id: int) -> PaymentModel:
        return self.db_session.query(PaymentModel).filter_by(id=payment_id).first()

    def find_by_payment_id(self, payment_id: str) -> PaymentModel:
        return self.db_session.query(PaymentModel).filter_by(payment_id=payment_id).first()

    def find_by_preference_id(self, preference_id: str) -> PaymentModel:
        return self.db_session.query(PaymentModel).filter_by(preference_id=preference_id).first()
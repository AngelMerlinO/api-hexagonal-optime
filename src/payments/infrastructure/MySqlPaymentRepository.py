
from src.payments.domain.PaymentRepository import PaymentRepository
from src.payments.domain.Payment import Payment
from sqlalchemy.orm import Session
from typing import List

class MySqlPaymentRepository(PaymentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, payment: Payment):
        self.db_session.add(payment)
        self.db_session.commit()
        self.db_session.refresh(payment)
        return payment

    def update(self, payment: Payment):
        self.db_session.commit()
        self.db_session.refresh(payment)
        return payment

    def find_by_id(self, payment_id: int) -> Payment:
        payment = self.db_session.query(Payment).filter_by(id=payment_id).first()
        return payment

    def find_by_payment_id(self, payment_id: str) -> Payment:
        payment = self.db_session.query(Payment).filter_by(payment_id=payment_id).first()
        return payment

    def find_by_preference_id(self, preference_id: str) -> Payment:
        payment = self.db_session.query(Payment).filter_by(preference_id=preference_id).first()
        return payment
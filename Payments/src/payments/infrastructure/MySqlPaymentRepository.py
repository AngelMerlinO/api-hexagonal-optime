from sqlalchemy.orm import Session
from src.payments.domain.PaymentRepository import PaymentRepository
from src.payments.domain.Payment import Payment
from src.payments.infrastructure.orm.PaymentModel import PaymentModel

class MySqlPaymentRepository(PaymentRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, payment: Payment):
        payment_model = PaymentModel(
            user_id=payment.user_id,
            preference_id=payment.preference_id,
            payment_id=payment.payment_id,
            status=payment.status,
            status_detail=payment.status_detail,
            amount=payment.amount,
            currency_id=payment.currency_id,
            description=payment.description,
            date_created=payment.date_created
        )
        self.db.add(payment_model)
        self.db.commit()
        self.db.refresh(payment_model)
        payment.id = payment_model.id
        return payment

    def update(self, payment: Payment):
        payment_model = self.db.query(PaymentModel).filter_by(id=payment.id).first()
        if not payment_model:
            raise ValueError(f"Payment with ID {payment.id} not found")

        payment_model.status = payment.status
        payment_model.status_detail = payment.status_detail
        payment_model.date_created = payment.date_created
        payment_model.payment_id = payment.payment_id

        self.db.commit()
        self.db.refresh(payment_model)

    def find_by_id(self, payment_id: int) -> Payment:
        payment_model = self.db.query(PaymentModel).filter_by(id=payment_id).first()
        if not payment_model:
            raise ValueError(f"Payment with ID {payment_id} not found")

        return Payment(
            id=payment_model.id,
            user_id=payment_model.user_id,
            preference_id=payment_model.preference_id,
            payment_id=payment_model.payment_id,
            amount=payment_model.amount,
            currency_id=payment_model.currency_id,
            description=payment_model.description,
            status=payment_model.status,
            status_detail=payment_model.status_detail,
            date_created=payment_model.date_created
        )

    def find_by_payment_id(self, payment_id: str) -> Payment:
        payment_model = self.db.query(PaymentModel).filter_by(payment_id=payment_id).first()
        if not payment_model:
            raise ValueError(f"Payment with payment_id {payment_id} not found")

        return Payment(
            id=payment_model.id,
            user_id=payment_model.user_id,
            preference_id=payment_model.preference_id,
            payment_id=payment_model.payment_id,
            amount=payment_model.amount,
            currency_id=payment_model.currency_id,
            description=payment_model.description,
            status=payment_model.status,
            status_detail=payment_model.status_detail,
            date_created=payment_model.date_created
        )

    def find_by_preference_id(self, preference_id: str) -> Payment:
        payment_model = self.db.query(PaymentModel).filter_by(preference_id=preference_id).first()
        if not payment_model:
            raise ValueError(f"Payment with preference_id {preference_id} not found")

        return Payment(
            id=payment_model.id,
            user_id=payment_model.user_id,
            preference_id=payment_model.preference_id,
            payment_id=payment_model.payment_id,
            amount=payment_model.amount,
            currency_id=payment_model.currency_id,
            description=payment_model.description,
            status=payment_model.status,
            status_detail=payment_model.status_detail,
            date_created=payment_model.date_created
        )

    def delete(self, payment_id: int):
        payment_model = self.db.query(PaymentModel).filter_by(id=payment_id).first()
        if not payment_model:
            raise ValueError(f"Payment with ID {payment_id} not found")

        self.db.delete(payment_model)
        self.db.commit()
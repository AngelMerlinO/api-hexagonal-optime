# src/payments/domain/Payment.py
from decimal import Decimal
from datetime import datetime

class Payment:
    def __init__(
        self,
        user_id: int,
        preference_id: str,
        amount: Decimal,
        currency_id: str,
        description: str = None,
        payment_id: str = None,
        status: str = None,
        status_detail: str = None,
        date_created: datetime = None,
        id: int = None
    ):
        self.id = id  # Agregamos el id
        self.user_id = user_id
        self.preference_id = preference_id
        self.amount = amount
        self.currency_id = currency_id
        self.description = description
        self.payment_id = payment_id
        self.status = status
        self.status_detail = status_detail
        self.date_created = date_created

    def __repr__(self):
        return f"<Payment {self.payment_id} for User {self.user_id}>"
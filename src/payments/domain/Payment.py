from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    preference_id = Column(String(255), nullable=False)
    payment_id = Column(String(255), nullable=True)
    status = Column(String(50), nullable=True)
    status_detail = Column(String(255), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency_id = Column(String(10), nullable=False)
    description = Column(String(255), nullable=True)
    date_created = Column(TIMESTAMP, nullable=True)  # Agregado
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    # Relación con User
    user = relationship('User', back_populates='payments')

    def __init__(
        self,
        user_id,
        preference_id,
        amount,
        currency_id,
        description=None,
        payment_id=None,
        status=None,
        status_detail=None,
        date_created=None
    ):
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
        return f"<Payment {self.id} for User {self.user_id}>"
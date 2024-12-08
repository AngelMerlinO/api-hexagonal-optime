from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship, composite
from sqlalchemy.sql import func
from config.database import Base
from src.payments.domain.Timestamp import Timestamps

class PaymentModel(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    preference_id = Column(String(255), nullable=False)
    payment_id = Column(String(255), nullable=True)
    status = Column(String(50), nullable=True)
    status_detail = Column(String(255), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency_id = Column(String(10), nullable=False)
    description = Column(String(255), nullable=True)
    date_created = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, nullable=True)

    timestamps = composite(Timestamps, created_at, updated_at, deleted_at)


    def __repr__(self):
        return f"<PaymentModel {self.id} for User {self.user_id}>"
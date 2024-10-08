from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class PaymentModel(Base):
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
    date_created = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    # Relación con UserModel, utilizando el nombre de la clase como cadena
    user = relationship('UserModel', back_populates='payments')

    def __repr__(self):
        return f"<PaymentModel {self.id} for User {self.user_id}>"
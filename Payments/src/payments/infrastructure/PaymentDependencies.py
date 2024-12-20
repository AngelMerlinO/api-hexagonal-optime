from sqlalchemy.orm import Session
from fastapi import Depends
from src.payments.infrastructure.MySqlPaymentRepository import MySqlPaymentRepository
from src.payments.infrastructure.RabbitMQ import RabbitMQ
from src.payments.application.services.PaymentService import PaymentService
from config.database import get_db

rabbitmq_publisher = RabbitMQ(
    host='52.72.86.85',
    queue='payment_success_queue',
    username='optimeroot',
    password='optimeroot'
)

def get_payment_service(db: Session = Depends(get_db)) -> PaymentService:
    payment_repository = MySqlPaymentRepository(db)
    
    payment_service = PaymentService(
        payment_repository=payment_repository,
        publisher=rabbitmq_publisher
    )
    
    return payment_service

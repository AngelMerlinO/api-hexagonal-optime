from sqlalchemy.orm import Session
from fastapi import Depends
from src.payments.infrastructure.MySqlPaymentRepository import MySqlPaymentRepository
from src.payments.infrastructure.RabbitMQ import RabbitMQ
from src.payments.application.services.PaymentService import PaymentService
from src.payments.infrastructure.MercadoPagoService import MercadoPagoService
from config.database import get_db

rabbitmq_publisher = RabbitMQ(
    host='34.236.102.207',
    queue='notifications_queue',
    username='usuario',
    password='password',
    routing_key='payment.created'
)

def get_payment_service(db: Session = Depends(get_db)) -> PaymentService:
    payment_repository = MySqlPaymentRepository(db)
    mercado_pago_service = MercadoPagoService() 

    payment_service = PaymentService(
        payment_repository=payment_repository,
        publisher=rabbitmq_publisher,
        mercado_pago_service=mercado_pago_service 
    )
    
    return payment_service
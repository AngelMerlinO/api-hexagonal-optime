from sqlalchemy.orm import Session
from fastapi import Depends
from src.contact.infraestructure.MySqlContactRepository import MySqlContactRepository
from src.contact.infraestructure.RabbitMQ import RabbitMQ
from src.contact.application.services.ContactService import ContactService
from config.database import get_db

rabbitmq_publisher = RabbitMQ(
    host='52.72.86.85',
    queue='contact_queue_create',
    username='optimeroot',
    password="optimeroot",
)

def get_contact_service(db: Session = Depends(get_db)) -> ContactService:
    contact_repository = MySqlContactRepository(db)
    
    contact_service = ContactService(
        contact_repository=contact_repository,
        publisher=rabbitmq_publisher
    )
    
    return contact_service


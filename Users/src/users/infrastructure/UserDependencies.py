# Importaciones necesarias
from sqlalchemy.orm import Session
from fastapi import Depends
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from src.contact.infraestructure.MySqlContactRepository import MySqlContactRepository
from src.users.infrastructure.RabbitMQ import RabbitMQ
from src.users.application.services.UserService import UserService
from config.database import get_db 

# Configuración de RabbitMQ como publicador
rabbitmq_publisher = RabbitMQ(
    host='34.236.102.207',
    queue='notifications_queue',
    username='usuario',
    password='password',
    routing_key='user.created'
)

# Inicialización del servicio de usuario con el publicador RabbitMQ
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repository = MySqlUserRepository(db)
    contact_repository = MySqlContactRepository(db)

    user_service = UserService(
        user_repository=user_repository,
        contact_repository=contact_repository,
        publisher=rabbitmq_publisher
    )
    
    return user_service
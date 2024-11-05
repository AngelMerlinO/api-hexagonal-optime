from sqlalchemy.orm import Session
from fastapi import Depends
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from src.contact.infraestructure.MySqlContactRepository import MySqlContactRepository
from src.users.infrastructure.RabbitMQ import RabbitMQ
from src.users.application.services.UserService import UserService
from config.database import get_db  # Función que retorna una sesión de la base de datos

# Configuración de RabbitMQ (solo una vez, fuera de la función)
rabbitmq_publisher = RabbitMQ(
    host='34.236.102.207',
    queue='user_created_queue',
    username='usuario',
    password='password'
)

# Dependencia para obtener una instancia de `UserService` configurada
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    # Crear instancias de los repositorios usando la sesión de base de datos
    user_repository = MySqlUserRepository(db)
    contact_repository = MySqlContactRepository(db)  # Asegúrate de tener esta implementación concreta

    # Crear instancia de UserService usando los repositorios y el publicador de RabbitMQ
    user_service = UserService(
        user_repository=user_repository,
        contact_repository=contact_repository,
        publisher=rabbitmq_publisher
    )
    
    return user_service
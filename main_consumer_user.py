import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "Users")))

from src.users.infrastructure.RabbitMQConsumer import RabbitMQConsumer

if __name__ == "__main__":
    consumer = RabbitMQConsumer(
        host='34.236.102.207',
        queue='user_created_queue',
        username='usuario',
        password='password'
    )
    try:
        print("Iniciando consumidor de eventos de usuario...")
        consumer.start_listening()
    except KeyboardInterrupt:
        print("Interrumpido por el usuario. Cerrando consumidor de User...")
    finally:
        consumer.close()

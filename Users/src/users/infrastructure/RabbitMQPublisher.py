# Users/src/users/infrastructure/RabbitMQPublisher.py
import pika
import json
from src.users.domain.EventPublisher import EventPublisher

class RabbitMQPublisher(EventPublisher):
    def __init__(self, host='34.236.102.207', queue='user_created_queue', username='usuario', password='password'):
        self.host = host
        self.queue = queue
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host=self.host, port=5672, credentials=credentials)
        
        # Establecer conexión y canal
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        # Declarar el exchange y la cola
        exchange_name = 'user_events_exchange'
        self.channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
        self.channel.queue_declare(queue=self.queue, durable=True)
        
        # Enlace entre el exchange y la cola
        routing_key = 'user.created'
        self.channel.queue_bind(exchange=exchange_name, queue=self.queue, routing_key=routing_key)
    
    def publish(self, message: dict):
        # Publicar el mensaje en RabbitMQ
        self.channel.basic_publish(
            exchange='user_events_exchange',
            routing_key='user.created',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # Hacer el mensaje persistente
        )
    
    def close(self):
        # Cerrar la conexión cuando ya no sea necesario
        self.connection.close()
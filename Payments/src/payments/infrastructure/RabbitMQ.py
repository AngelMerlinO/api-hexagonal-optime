# Users/src/users/infrastructure/RabbitMQ.py
import pika
import json
from src.payments.domain.EventPublisher import EventPublisher

class RabbitMQ(EventPublisher):
    def __init__(self, host='34.236.102.207', queue='payment_success_queue', username='usuario', password='password'):
        self.host = host
        self.queue = queue
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host=self.host, port=5672, credentials=credentials)
        
        # Establecer conexión y canal
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        # Declarar el exchange y la cola
        exchange_name = 'payment_events_exchange'
        self.channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
        self.channel.queue_declare(queue=self.queue, durable=True)
        
        # Enlace entre el exchange y la cola
        routing_key = 'payment.created'
        self.channel.queue_bind(exchange=exchange_name, queue=self.queue, routing_key=routing_key)
    
    def publish(self, message: dict):
        # Publicar el mensaje en RabbitMQ
        self.channel.basic_publish(
            exchange='payment_events_exchange',
            routing_key='payment.created',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # Hacer el mensaje persistente
        )
        #funcion de escucha 
    
    def close(self):
        # Cerrar la conexión cuando ya no sea necesario
        self.connection.close()
import pika
import json
from src.payments.domain.EventPublisher import EventPublisher

class RabbitMQ(EventPublisher):
    def __init__(self, host='52.72.86.85', queue='notifications_queue', username='optimeroot', password='optimeroot', routing_key='user.created'):
        self.host = host
        self.queue = queue
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host=self.host, port=5672, credentials=credentials)
        
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        # Configuración del Exchange y Cola de Notificaciones
        exchange_name = 'notifications_exchange'
        self.channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
        self.channel.queue_declare(queue=self.queue, durable=True)
        
        # Bind de la cola con ambas Routing Keys
        self.channel.queue_bind(exchange=exchange_name, queue=self.queue, routing_key='payment.created')
    
    def publish(self, message: dict, routing_key: str):
        self.channel.basic_publish(
            exchange='notifications_exchange',
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )
    
    def close(self):
        self.connection.close()
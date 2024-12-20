import pika
import json
from src.contact.domain.EventPublisher import EventPublisher

class RabbitMQ(EventPublisher):
    def __init__(self, host='52.72.86.85', queue='contact_queue_create', username='optimeroot', password='optimeroot'):
        self.host = host
        self.queue = queue
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host=self.host, port=5672, credentials=credentials)
        
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        exchange_name = 'contact_exchange'
        self.channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
        self.channel.queue_declare(queue=self.queue, durable=True)
        
        routing_key = 'contact.created'
        self.channel.queue_bind(exchange=exchange_name, queue=self.queue, routing_key=routing_key)
        
    def publish(self, message: dict):
        self.channel.basic_publish(
            exchange='contact_exchange',
            routing_key='contact.created',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )
            
    def close(self):
        self.connection.close()
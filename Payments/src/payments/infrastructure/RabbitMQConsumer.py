import pika
import json

class RabbitMQConsumer:
    def __init__(self, host='52.72.86.85', queue='payment_success_queue', username='usuario', password='password'):
        self.host = host
        self.queue = queue
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionsParameters(host=self.host, port=5672, credentials=credentials)
        
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue=self.queue, durable=True)
      
        
    def start_listening(self):
        def callback(ch, method, properties, body):
            message = json.loads(body)
            self.event_hanlder.handle_payment(message)
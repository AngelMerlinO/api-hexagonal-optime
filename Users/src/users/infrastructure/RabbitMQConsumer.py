import pika
import json
from src.users.application.services.UserEventHandler import UserEventHandler

class RabbitMQConsumer:
    def __init__(self, host='34.236.102.207', queue='user_created_queue', username='usuario', password='password'):
        self.host = host
        self.queue = queue
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host=self.host, port=5672, credentials=credentials)
        
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.event_handler = UserEventHandler()

    def start_listening(self):
        def callback(ch, method, properties, body):
            message = json.loads(body)
            self.event_handler.handle_user_created_event(message)

        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
        print("Listening for User events...")
        self.channel.start_consuming()

    def close(self):
        self.connection.close()

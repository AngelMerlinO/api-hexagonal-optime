import json
import pika
from src.notifications.application.services import NotificationService

class NotificationConsumer:
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    def _process_payment_message(self, ch, method, properties, body):
        # Procesar mensajes de la cola payment_success_queue
        event_data = json.loads(body)
        print("Mensaje de pago recibido:", event_data)

        # Crear una notificación para el pago
        self.notification_service.create_notification(
            user_id=event_data["user_id"],
            title=event_data["title"],
            content=event_data["message"],
            type=event_data["type"],
            service_type=event_data["service_type"],  # Pasar service_type correctamente
            link=event_data["link"]
        )

    def _process_user_message(self, ch, method, properties, body):
        # Procesar mensajes de la cola user_created_queue
        event_data = json.loads(body)
        print("Mensaje de usuario recibido:", event_data)

        # Crear una notificación para el usuario
        self.notification_service.create_notification(
            user_id=event_data["user_id"],
            title=event_data["title"],
            content=event_data["message"],
            type=event_data["type"],
            service_type=event_data["service_type"],  # Pasar service_type correctamente
            link=event_data["link"]
        )

    def start_consuming(self):
        # Configurar conexión con RabbitMQ con host y credenciales
        credentials = pika.PlainCredentials('usuario', 'password')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='34.236.102.207', credentials=credentials)
        )
        channel = connection.channel()

        # Declarar intercambios y colas con durable=True
        channel.exchange_declare(exchange='payment_events_exchange', exchange_type='direct', durable=True)
        channel.exchange_declare(exchange='user_events_exchange', exchange_type='direct', durable=True)
        
        # Declarar colas y enlazarlas a los intercambios correspondientes con claves de enrutamiento
        channel.queue_declare(queue='payment_success_queue', durable=True)
        channel.queue_declare(queue='user_created_queue', durable=True)
        channel.queue_bind(exchange='payment_events_exchange', queue='payment_success_queue', routing_key='payment.created')
        channel.queue_bind(exchange='user_events_exchange', queue='user_created_queue', routing_key='user.created')

        # Configurar la recepción de mensajes de ambas colas con sus respectivos callbacks
        channel.basic_consume(queue='payment_success_queue', on_message_callback=self._process_payment_message, auto_ack=True)
        channel.basic_consume(queue='user_created_queue', on_message_callback=self._process_user_message, auto_ack=True)

        print("Esperando mensajes en las colas de eventos de pago y usuario...")
        channel.start_consuming()
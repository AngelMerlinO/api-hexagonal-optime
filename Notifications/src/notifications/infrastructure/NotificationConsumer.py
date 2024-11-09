import json
import pika
from src.notifications.application.services import NotificationService

class NotificationConsumer:
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    def _process_message(self, ch, method, properties, body):
        # Cargar datos del mensaje
        event_data = json.loads(body)
        routing_key = method.routing_key

        # Procesar mensajes basados en la routing_key
        if routing_key == 'user.created':
            print("Mensaje de usuario recibido:", event_data)
            # Crear notificación para usuario creado
            self.notification_service.create_notification(
                user_id=event_data["user_id"],
                title=event_data["title"],
                content=event_data["message"],
                type=event_data["type"],
                service_type=event_data["service_type"],
                link=event_data["link"]
            )
        elif routing_key == 'payment.created':
            print("Mensaje de pago recibido:", event_data)
            # Crear notificación para pago exitoso
            self.notification_service.create_notification(
                user_id=event_data["user_id"],
                title=event_data["title"],
                content=event_data["message"],
                type=event_data["type"],
                service_type=event_data["service_type"],
                link=event_data["link"]
            )

    def start_consuming(self):
        # Configurar conexión con RabbitMQ
        credentials = pika.PlainCredentials('usuario', 'password')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='34.236.102.207', credentials=credentials)
        )
        channel = connection.channel()

        # Declarar el exchange y la cola de notificaciones
        channel.exchange_declare(exchange='notifications_exchange', exchange_type='direct', durable=True)
        channel.queue_declare(queue='notifications_queue', durable=True)
        
        # Bind de la cola a las routing keys necesarias
        channel.queue_bind(exchange='notifications_exchange', queue='notifications_queue', routing_key='user.created')
        channel.queue_bind(exchange='notifications_exchange', queue='notifications_queue', routing_key='payment.created')

        # Consumir mensajes de la cola `notifications_queue`
        channel.basic_consume(queue='notifications_queue', on_message_callback=self._process_message, auto_ack=True)

        print("Esperando mensajes en notifications_queue...")
        channel.start_consuming()
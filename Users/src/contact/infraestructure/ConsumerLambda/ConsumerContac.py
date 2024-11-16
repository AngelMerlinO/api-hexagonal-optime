import json
import pika
import requests
import time

class ContactConsumer:
    def __init__(self, max_retries=5):
        # Configuración de conexión a RabbitMQ
        credentials = pika.PlainCredentials('usuario', 'password')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='34.236.102.207', credentials=credentials)
        )
        self.channel = self.connection.channel()
        self.max_retries = max_retries  # Número máximo de reintentos antes de enviar a la DLQ

    def _process_contact_message(self, ch, method, properties, body):
        event_data = json.loads(body)
        print("Mensaje de contacto recibido:", event_data)

        payload = {
            "contact_id": event_data.get("id", 1),
            "email": event_data.get("email")
        }

        # URL de la función Lambda
        LAMBDA_URL = 'https://2qwsze5abp5zlz64shmy2tppey0asecr.lambda-url.us-east-1.on.aws/'

        for attempt in range(self.max_retries):
            try:
                response = requests.post(LAMBDA_URL, json=payload, headers={'Content-Type': 'application/json'})
                response.raise_for_status()
                print("Invocación de Lambda exitosa:", response.json())
                ch.basic_ack(delivery_tag=method.delivery_tag)  # Marcar como procesado
                return
            except requests.exceptions.RequestException as e:
                print(f"Error al invocar Lambda (intento {attempt + 1}/{self.max_retries}):", e)
                time.sleep(2 ** attempt)  # Retraso exponencial en cada reintento

        # Si llega aquí, ha fallado después de max_retries intentos; enviar a la DLQ o registrar el error
        print("No se pudo procesar el mensaje después de múltiples intentos. Enviando a la DLQ.")
        self._send_to_dead_letter_queue(event_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Marcar como procesado para evitar ciclo infinito

    def _send_to_dead_letter_queue(self, event_data):
        # Este método maneja la lógica de enviar el mensaje a una DLQ o registrarlo
        dlq_name = 'contact_dead_letter_queue'
        self.channel.queue_declare(queue=dlq_name, durable=True)
        self.channel.basic_publish(exchange='', routing_key=dlq_name, body=json.dumps(event_data))
        print("Mensaje enviado a la Dead Letter Queue:", event_data)

    def start_consuming(self):
        self.channel.exchange_declare(exchange='contact_exchange', exchange_type='direct', durable=True)
        self.channel.queue_declare(queue='contact_queue_create', durable=True)
        self.channel.queue_bind(exchange='contact_exchange', queue='contact_queue_create', routing_key='contact.created')

        self.channel.basic_consume(queue='contact_queue_create', on_message_callback=self._process_contact_message)
        print("Esperando mensajes en la cola de contactos...")
        self.channel.start_consuming()
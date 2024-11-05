# Users/src/users/infrastructure/rabbitmq_setup.py
import pika

def setup_rabbitmq():
    # Configurar credenciales y parámetros de conexión
    credentials = pika.PlainCredentials('usuario', 'password')  # Reemplaza 'usuario' y 'password' con tus credenciales
    parameters = pika.ConnectionParameters(
        host='34.236.102.207',  # Dirección IP pública de tu instancia EC2
        port=5672,  # Puerto AMQP predeterminado de RabbitMQ
        credentials=credentials
    )

    try:
        # Establecer conexión
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        # Declaración del exchange
        exchange_name = 'user_events_exchange'
        channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
        
        # Declaración de la cola
        queue_name = 'user_created_queue'
        channel.queue_declare(queue=queue_name, durable=True)
        
        # Enlace entre el exchange y la cola con la routing key
        routing_key = 'user.created'
        channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
        
        print("RabbitMQ setup completed.")
        
    except pika.exceptions.AMQPConnectionError as e:
        print("Error al conectar con RabbitMQ:", str(e))
    finally:
        # Cerrar la conexión si está abierta
        if connection and connection.is_open:
            connection.close()
            print("Conexión cerrada exitosamente")

if __name__ == "__main__":
    setup_rabbitmq()
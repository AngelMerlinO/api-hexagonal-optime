const amqp = require('amqplib');

async function consume() {
    try {
        // Configuración de conexión
        const user = 'optimeroot';
        const password = 'optimeroot';
        const host = '52.72.86.85';
        const queue = 'messages_queue';
        const exchange = 'messages_exchange';
        const routingKey = 'messages.key';

        // URI de conexión AMQP
        const amqpUrl = `amqp://${user}:${password}@${host}`;

        // Conexión al servidor RabbitMQ
        const connection = await amqp.connect(amqpUrl);
        console.log('Conexión exitosa a RabbitMQ');

        // Crear un canal
        const channel = await connection.createChannel();

        // Asegurar que la cola existe
        await channel.assertQueue(queue, {
            durable: true, // Cola persistente
        });

        // Vincular la cola al exchange
        await channel.bindQueue(queue, exchange, routingKey);

        console.log(`Esperando mensajes en la cola: ${queue}`);

        // Consumir mensajes de la cola
        await channel.consume(queue, (message) => {
            if (message !== null) {
                const content = message.content;
                console.log(`Mensaje recibido: ${content}`);

                // Confirmar recepción del mensaje
                channel.ack(message);
            } else {
                console.log('Mensaje nulo recibido');
            }
        });
    } catch (error) {
        console.error('Error al consumir mensajes:', error);
    }
}

// Ejecutar el consumidor
consume();

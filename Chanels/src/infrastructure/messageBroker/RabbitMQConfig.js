const amqp = require('amqplib');
require('dotenv').config();

class RabbitMQConfig {
    constructor() {
        this.connection = null;
        this.channel = null;
        this.exchange = process.env.RABBITMQ_EXCHANGE || 'messages_exchange';
        this.queue = process.env.RABBITMQ_QUEUE || 'messages_queue';
        this.routingKey = process.env.RABBITMQ_ROUTING_KEY || 'messages.key';
        this.rabbitmqUrl = `amqp://${process.env.RABBITMQ_USER || 'optimeroot'}:${process.env.RABBITMQ_PASSWORD || 'optimeroot'}@${process.env.RABBITMQ_HOST || '52.72.86.85'}`;
    }

    // Método para conectar a RabbitMQ
    async connect() {
        try {
            console.log('Connecting to RabbitMQ...');
            this.connection = await amqp.connect(this.rabbitmqUrl);
            this.channel = await this.connection.createChannel();

            // Configurar el exchange principal
            await this.channel.assertExchange(this.exchange, 'fanout', { durable: true });

            // Configurar la cola principal
            await this.channel.assertQueue(this.queue, { durable: true });
            await this.channel.bindQueue(this.queue, this.exchange, this.routingKey);

            console.log(`RabbitMQ connected. Exchange: ${this.exchange}, Queue: ${this.queue}, Routing Key: ${this.routingKey}`);
        } catch (error) {
            console.error('Failed to connect to RabbitMQ:', error.message);
            setTimeout(() => this.connect(), 5000); // Intentar reconectar tras un fallo
        }
    }

    // Método para publicar en la cola principal
    async publish(message) {
        if (!this.channel) {
            throw new Error('RabbitMQ channel is not initialized');
        }

        try {
            const bufferMessage = Buffer.from(JSON.stringify(message));
            this.channel.publish(this.exchange, this.routingKey, bufferMessage);
            console.log(`Message published to exchange ${this.exchange} with routing key ${this.routingKey}`);
        } catch (error) {
            console.error('Failed to publish message:', error.message);
        }
    }

    // Método para publicar en la cola de eliminación
    async publishToDeleteQueue(message) {
        if (!this.channel) {
            throw new Error('RabbitMQ channel is not initialized');
        }

        try {
            const deleteQueue = 'messages_queue'; // Nombre de la cola para eliminaciones
            const deleteRoutingKey = 'delete.key'; // Clave de enrutamiento para eliminaciones

            // Asegurar la cola y su vínculo con el exchange
            await this.channel.assertQueue(deleteQueue, { durable: true });
            await this.channel.bindQueue(deleteQueue, this.exchange, deleteRoutingKey);

            // Publicar el mensaje
            const bufferMessage = Buffer.from(JSON.stringify(message));
            this.channel.publish(this.exchange, deleteRoutingKey, bufferMessage);

            console.log(`Message published to delete queue with routing key: ${deleteRoutingKey}`);
        } catch (error) {
            console.error('Failed to publish to delete queue:', error.message);
        }
    }

    // Método para cerrar la conexión
    async close() {
        try {
            if (this.channel) await this.channel.close();
            if (this.connection) await this.connection.close();
            console.log('RabbitMQ connection closed.');
        } catch (error) {
            console.error('Failed to close RabbitMQ connection:', error.message);
        }
    }
}

module.exports = new RabbitMQConfig();
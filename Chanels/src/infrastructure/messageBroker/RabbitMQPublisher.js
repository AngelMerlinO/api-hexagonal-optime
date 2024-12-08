const amqp = require('amqplib');

class RabbitMQPublisher {
    constructor() {
        this.exchange = 'messages_exchange'; // Exchange configurado para todas las publicaciones
        this.rabbitmqUrl = 'amqp://optimeroot:optimeroot@52.72.86.85'; // Credenciales de RabbitMQ
    }

    async connect() {
        try {
            console.log('Connecting to RabbitMQ...');
            // Conexión con RabbitMQ
            this.connection = await amqp.connect(this.rabbitmqUrl);
            this.channel = await this.connection.createChannel();

            // Configurar el exchange
            await this.channel.assertExchange(this.exchange, 'fanout', { durable: true });

            console.log('RabbitMQ connected.');
        } catch (error) {
            console.error('Failed to connect to RabbitMQ:', error.message);
            throw error;
        }
    }

    async publishToDeleteQueue(message) {
        if (!this.channel) {
            throw new Error('RabbitMQ channel is not initialized');
        }

        try {
            // Publicar en la cola de eliminación
            const routingKey = 'delete.key';
            const queue = 'messages_queue';
            await this.channel.assertQueue(queue, { durable: true });
            await this.channel.bindQueue(queue, this.exchange, routingKey);

            this.channel.publish(this.exchange, routingKey, Buffer.from(JSON.stringify(message)));
            console.log(`Message published to delete queue with routing key: ${routingKey}`);
        } catch (error) {
            console.error('Failed to publish to delete queue:', error.message);
            throw error;
        }
    }

    async publish(message, routingKey) {
        if (!this.channel) {
            throw new Error('RabbitMQ channel is not initialized');
        }

        try {
            this.channel.publish(this.exchange, routingKey, Buffer.from(JSON.stringify(message)));
            console.log(`Message published to exchange ${this.exchange} with routing key ${routingKey}`);
        } catch (error) {
            console.error('Failed to publish message:', error.message);
            throw error;
        }
    }

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

module.exports = new RabbitMQPublisher();
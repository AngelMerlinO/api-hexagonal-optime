const RabbitMQConfig = require('../../infrastructure/messageBroker/RabbitMQConfig');
const MessageRepository = require('../../infrastructure/repositories/MessageRepository');

class PublishMessage {
    async execute(message) {

        // Guardar el mensaje en la base de datos
        await MessageRepository.saveMessage(message);

        // Publicar el mensaje en RabbitMQ
        await RabbitMQConfig.publish( message);
    }
}

module.exports = PublishMessage;
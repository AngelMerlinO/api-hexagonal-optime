const MessageRepository = require('../../infrastructure/repositories/MessageRepository');
const RabbitMQConfig = require('../../infrastructure/messageBroker/RabbitMQConfig');

class DeleteMessage {
    async execute(messageId) {
        try {
            // Eliminar el mensaje de la base de datos
            await MessageRepository.deleteMessageById(messageId);

            // Crear un evento de eliminación
            const deleteEvent = {
                messageId: messageId,
                event: 'MessageDeleted',
                timestamp: new Date(),
            };

            // Publicar el evento en la cola de eliminación
            await RabbitMQConfig.publishToDeleteQueue(deleteEvent);

            return { success: true, message: `Message with ID ${messageId} deleted successfully and event published.` };
        } catch (error) {
            console.error(`Error deleting message with ID ${messageId}:`, error.message);
            throw error;
        }
    }
}

module.exports = DeleteMessage;
const MessageRepository = require('../../infrastructure/repositories/MessageRepository');

class GetAllMessages {
    async execute() {
        try {
            const messages = await MessageRepository.getAllMessages();
            return messages;
        } catch (error) {
            console.error('Error fetching messages:', error.message);
            throw error;
        }
    }
}

module.exports = GetAllMessages;
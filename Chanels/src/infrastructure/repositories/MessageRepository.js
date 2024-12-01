const connectToDatabase = require('../database/DatabaseConfig');

class MessageRepository {
    async saveMessage(message) {
        try {
            const connection = await connectToDatabase();
            const query = `
                INSERT INTO messages (subject, username, content, contact, timestamp)
                VALUES (?, ?, ?, ?, ?)
            `;
            const values = [
                message.subject,
                message.username,
                message.content,
                message.contact,
                message.timestamp,
            ];

            await connection.execute(query, values);
            console.log('Message saved successfully.');
        } catch (error) {
            console.error('Failed to save message:', error.message);
            throw error;
        }
    }

    
    async deleteMessageById(messageId) {
        try {
            const connection = await connectToDatabase();
            const query = 'DELETE FROM messages WHERE id = ?';
            const [result] = await connection.execute(query, [messageId]);

            if (result.affectedRows === 0) {
                throw new Error(`No message found with ID: ${messageId}`);
            }

            console.log(`Message with ID: ${messageId} deleted successfully.`);
        } catch (error) {
            console.error('Failed to delete message:', error.message);
            throw error;
        }
    }

    async getAllMessages() {
        try {
            const connection = await connectToDatabase();
            const [rows] = await connection.execute('SELECT * FROM messages');
            return rows;
        } catch (error) {
            console.error('Failed to fetch messages:', error.message);
            throw error;
        }
    }
}

module.exports = new MessageRepository();
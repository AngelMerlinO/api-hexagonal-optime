const express = require('express');
const router = express.Router();
const PublishMessage = require('../../application/useCases/PublishMessage');
const DeleteMessage = require('../../application/useCases/DeleteMessage');
const GetAllMessages = require('../../application/useCases/GetAllMessages');
const Message = require('../../domain/entities/Message');

const publishMessage = new PublishMessage();
const deleteMessage = new DeleteMessage();
const getAllMessages = new GetAllMessages();

router.post('/message', async (req, res) => {
    const { subject, username, content, contact } = req.body;

    try {
        const message = new Message(subject, username, content, contact);
        await publishMessage.execute(message);
        res.status(200).send({ success: true, message: 'Message published successfully' });
    } catch (error) {
        console.error('Error publishing message:', error.message);
        res.status(500).send({ success: false, error: error.message });
    }
});

// Ruta para eliminar un mensaje por ID
router.delete('/delete/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const result = await deleteMessage.execute(id);
        res.status(200).send(result);
    } catch (error) {
        res.status(500).send({ success: false, error: error.message });
    }
});
router.get('/messages', async (req, res) => {
    try {
        const messages = await getAllMessages.execute();
        res.status(200).send({ success: true, data: messages });
    } catch (error) {
        res.status(500).send({ success: false, error: error.message });
    }
});
module.exports = router;
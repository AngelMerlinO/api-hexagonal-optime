const app = require('./app');
const RabbitMQConfig = require('./src/infrastructure/messageBroker/RabbitMQConfig');

const PORT = process.env.PORT || 3000;
const HOST = '0.0.0.0'; // Escuchar en todas las interfaces

(async () => {
    try {
        // Conectar a RabbitMQ
        await RabbitMQConfig.connect();

        // Inicia el servidor
        app.listen(PORT, HOST, () => {
            console.log(`Server is running on http://${HOST}:${PORT}`);
        });
    } catch (error) {
        console.error('Failed to start the application:', error.message);
        process.exit(1);
    }
})();
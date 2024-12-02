require('dotenv').config(); // Cargar las variables de entorno desde el archivo .env
const fs = require('fs');
const https = require('https');
const app = require('./app');
const RabbitMQConfig = require('./src/infrastructure/messageBroker/RabbitMQConfig');

const PORT = process.env.PORT || 4005;
const HOST = '0.0.0.0'; // Escuchar en todas las interfaces

(async () => {
    try {
        // Conectar a RabbitMQ
        await RabbitMQConfig.connect();

        // Obtener las rutas de los certificados desde las variables de entorno
        const certPath = process.env.SSL_CERTFILE;
        const keyPath = process.env.SSL_KEYFILE;

        // Asegúrate de que las rutas de los certificados estén configuradas
        if (!certPath || !keyPath) {
            throw new Error('Missing SSL certificate or key file path in environment variables.');
        }

        // Cargar los certificados SSL
        const options = {
            cert: fs.readFileSync(certPath),  // Lee el certificado desde la ruta definida en el .env
            key: fs.readFileSync(keyPath),    // Lee la clave desde la ruta definida en el .env
        };

        // Iniciar el servidor HTTPS
        https.createServer(options, app).listen(PORT, HOST, () => {
            console.log(`Server is running on https://${HOST}:${PORT}`);
        });
    } catch (error) {
        console.error('Failed to start the application:', error.message);
        process.exit(1);
    }
})();

const express = require('express');
const cors = require('cors');

const app = express();

// Configurar CORS
app.use(cors());
app.use(express.json());

// Tus rutas
app.use('/api/v1', require('./src/infrastructure/routes/PublishRouter'));

module.exports = app;
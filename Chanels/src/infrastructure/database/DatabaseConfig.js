const mysql = require('mysql2/promise');
require('dotenv').config();

const dbConfig = {
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port: process.env.DB_PORT,
};

let connection;

async function connectToDatabase() {
    if (!connection) {
        try {
            console.log('Connecting to MySQL...');
            connection = await mysql.createConnection(dbConfig);
            console.log('Connected to MySQL successfully.');
        } catch (error) {
            console.error('Failed to connect to MySQL:', error.message);
            throw error;
        }
    }
    return connection;
}

module.exports = connectToDatabase;
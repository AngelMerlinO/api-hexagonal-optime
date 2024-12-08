-- Crear la base de datos si no existe
CREATE DATABASE optimeusers;

-- Crear el usuario y asignar la contraseña
CREATE USER optimeroot WITH PASSWORD 'optimetest';

-- Otorgar todos los privilegios al usuario sobre la base de datos
GRANT ALL PRIVILEGES ON DATABASE optimeusers TO optimeroot;
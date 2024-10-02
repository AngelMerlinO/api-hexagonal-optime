-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS optime;

-- Crear el usuario y asignar la contraseña
CREATE USER IF NOT EXISTS 'optimeroot'@'localhost' IDENTIFIED BY 'optimetest';

-- Otorgar todos los privilegios al usuario sobre la base de datos optime
GRANT ALL PRIVILEGES ON optime.* TO 'optimeroot'@'localhost';

-- Aplicar los cambios de privilegios
FLUSH PRIVILEGES;
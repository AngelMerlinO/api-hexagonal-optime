-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS optime;

-- Crear el usuario y asignar la contraseña
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'optimeroot';

-- Otorgar todos los privilegios al usuario sobre la base de datos optimeactivities
GRANT ALL PRIVILEGES ON optime.* TO 'admin'@'localhost';

-- Aplicar los cambios de privilegios
FLUSH PRIVILEGES;
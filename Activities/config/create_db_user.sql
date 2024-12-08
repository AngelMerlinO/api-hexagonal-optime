-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS optimeactivities;

-- Crear el usuario y asignar la contraseña
CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'root';

-- Otorgar todos los privilegios al usuario sobre la base de datos optimeactivities
GRANT ALL PRIVILEGES ON optimeactivities.* TO 'root'@'localhost';

-- Aplicar los cambios de privilegios
FLUSH PRIVILEGES;
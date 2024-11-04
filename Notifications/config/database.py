import os
from pymongo import MongoClient
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

# Cargar las variables de entorno desde el archivo .env
load_dotenv("config/.env", encoding="utf-8")

Base = declarative_base()

# Leer las variables de entorno para la conexión a MongoDB
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', '27017')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Codificar el usuario y la contraseña si contienen caracteres especiales
DB_USER_ENCODED = quote_plus(DB_USER) if DB_USER else ''
DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD) if DB_PASSWORD else ''

# Construir la URL de conexión para MongoDB
DATABASE_URL = f"mongodb://{DB_USER_ENCODED}:{DB_PASSWORD_ENCODED}@{MONGO_HOST}:{MONGO_PORT}/{DB_NAME}"

# Conectar a MongoDB
client = MongoClient(DATABASE_URL)
db = client[DB_NAME]

# Función para obtener la base de datos
def get_mongo_collection():
    return db['notifications']


import os
from pymongo import MongoClient
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar las variables de entorno desde el archivo .env
load_dotenv("config/.env", encoding="utf-8")

Base = declarative_base()

# Leer las variables de entorno para la conexión a MongoDB
MONGO_DB = os.getenv('MONGO_DB')
DB_NAME = os.getenv('DB_NAME')

# Conectar a MongoDB utilizando la URI completa
client = MongoClient(MONGO_DB)
db = client[DB_NAME]

# Función para obtener la colección de MongoDB
def get_mongo_collection():
    return db['notifications']
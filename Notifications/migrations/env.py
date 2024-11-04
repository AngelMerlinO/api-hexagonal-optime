from pymongo import MongoClient

# Conexión a MongoDB
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DB_NAME = 'optime'
DB_USER = 'optimeroot'
DB_PASSWORD = 'optimetest'

client = MongoClient(f'mongodb://{DB_USER}:{DB_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{DB_NAME}')
db = client[DB_NAME]

# Crear colección e índices
def initialize_notifications_collection():
    if 'notifications' not in db.list_collection_names():
        db.create_collection('notifications')
    db.notifications.create_index("uuid", unique=True)

# Llamar a la función
if __name__ == "__main__":
    initialize_notifications_collection()
    print("La colección y los índices de 'notifications' han sido inicializados.")

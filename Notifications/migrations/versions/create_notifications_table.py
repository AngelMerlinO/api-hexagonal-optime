from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# Configuración de conexión
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DB_NAME = 'optime'
DB_USER = 'optimeroot'
DB_PASSWORD = 'optimetest'

# Conectar a MongoDB
client = MongoClient(f'mongodb://{DB_USER}:{DB_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{DB_NAME}')
db = client[DB_NAME]

# Crear la colección de "notifications" y definir su estructura
def create_notifications_collection():
    # Verifica si la colección ya existe
    if 'notifications' not in db.list_collection_names():
        db.create_collection('notifications')
        print("Colección 'notifications' creada exitosamente.")
    else:
        print("La colección 'notifications' ya existe.")

    # Definir los índices únicos o necesarios
    db.notifications.create_index("uuid", unique=True)
    
    # Documento de ejemplo para probar la estructura
    sample_notification = {
        "_id": ObjectId(),
        "uuid": str(ObjectId()),
        "user_id": ObjectId(),
        "title": "Sample Title",
        "message": "This is a sample notification message",
        "type": "email",
        "status": "pending",
        "link": "http://example.com",
        "sent_at": None,
        "created_at": datetime.now().astimezone(),
        "updated_at": datetime.now().astimezone(), 
        "deleted_at": None,
    }

    # Inserta un documento de ejemplo para confirmar que la colección se maneja correctamente
    try:
        db.notifications.insert_one(sample_notification)
        print("Documento insertado en la colección 'notifications'.")
    except Exception as e:
        print("Error al insertar el documento:", e)

# Ejecutar el script de creación de la colección
if __name__ == "__main__":
    create_notifications_collection()

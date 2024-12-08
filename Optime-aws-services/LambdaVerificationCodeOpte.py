import json
import time
from pymongo import MongoClient, errors

MONGO_URI = "mongodb+srv://221255:test@cluster0.phcgo8g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URI)
    db = client["optime-two-factor"]
    collection = db["twofactor"]
except errors.ConnectionFailure as e:
    raise Exception(f"Error de conexión a MongoDB Atlas: {e}")
except errors.ConfigurationError as e:
    raise Exception(f"Error de configuración de MongoDB: {e}")

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        contact_id = body.get('contact_id')
        otp = body.get('otp')

        if not contact_id or not otp:
            return response(400, 'contact_id y otp son requeridos')

        try:
            contact_id = int(contact_id)
        except ValueError:
            return response(400, 'contact_id debe ser un número válido')

        result = collection.find_one({'contact_id': contact_id})

        if not result:
            return response(404, 'código no encontrado')

        if result.get('verified_at'):
            return response(200, 'El código ya ha sido verificado anteriormente')

        if result['otp'] != otp:
            return response(401, 'código incorrecto')

        if result['expires_at'] < int(time.time()):
            return response(410, 'código expirado')

        verified_at = int(time.time())
        collection.update_one(
            {'contact_id': contact_id},
            {'$set': {'verified_at': verified_at}}
        )

        return response(200, 'código verificado correctamente')

    except errors.PyMongoError as e:
        return response(500, f'Error al validar el OTP: {str(e)}')

def response(status_code, message):
    return {
        'statusCode': status_code,
        'body': json.dumps({'message': message})
    }
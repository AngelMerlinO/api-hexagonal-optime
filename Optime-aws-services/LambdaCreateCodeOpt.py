import json
import random
import time
import requests
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
EMAIL_SERVICE_URL = os.getenv('EMAIL_SERVICE_URL')

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
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event

        contact_id = body.get('contact_id')
        email = body.get('email')

        if not contact_id or not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'contact_id y email son requeridos'})
            }

        otp = str(random.randint(100000, 999999))
        expiration = int(time.time()) + 300

        collection.insert_one({
            "contact_id": contact_id,
            "otp": otp,
            "expires_at": expiration,
            "verified_at": None  
        })

        subject = "Código OTP de Optime"
        email_body = f"""
        <html>
        <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            h2 {{
                color: #333333;
                text-align: center;
            }}
            p {{
                color: #555555;
                font-size: 16px;
            }}
            .otp {{
                font-size: 24px;
                color: #008CBA;
                text-align: center;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 12px;
                color: #999999;
            }}
        </style>
        </head>
        <body>
            <div class="container">
                <h2>Bienvenido a Optime</h2>
                <p>Tu código OTP es:</p>
                <div class="otp"><strong>{otp}</strong></div>
                <p>Este código es válido por 5 minutos. No lo compartas con nadie.</p>
                <p>Gracias por usar nuestra aplicación.</p>
                <div class="footer">
                    <p>Atentamente,</p>
                    <p><strong>Equipo de Optime</strong></p>
                </div>
            </div>
        </body>
        </html>
        """

        email_payload = {
            "email": email,
            "subject": subject,
            "body": email_body
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(EMAIL_SERVICE_URL, json=email_payload, headers=headers)

        if response.status_code == 200:
            return {
                'statusCode': 201,
                'body': json.dumps({
                    'otp': otp,
                    'message': 'OTP generado y correo enviado exitosamente'
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Error al enviar el correo'})
            }

    except errors.OperationFailure:
        return {
            'statusCode': 401,
            'body': json.dumps({'message': 'Autenticación fallida con MongoDB'})
        }

    except errors.PyMongoError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al guardar el OTP'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error inesperado: {str(e)}'})
        }
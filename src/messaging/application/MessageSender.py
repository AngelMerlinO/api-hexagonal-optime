import os
import requests
import json
from src.messaging.domain.Message import Message
from src.messaging.domain.MessageRepository import MessageRepository
from src.messaging.domain.exceptions import MessageSendingException

class MessageSender:
    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')  # Token de acceso almacenado en variable de entorno
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')  # Phone Number ID almacenado en variable de entorno
        self.url = f'https://graph.facebook.com/v20.0/{self.phone_number_id}/messages'

    def send_whatsapp_message(self, recipient_phone_number: str, message_content: str) -> Message:
        # Crear el objeto de mensaje
        message = Message(
            recipient_phone_number=recipient_phone_number,
            message_type="template",  # Establecemos 'template' como tipo de mensaje
            message_content=message_content,
            status="sending"
        )
        self.message_repository.save(message)

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # Cuerpo de la solicitud que será enviado a la API de Facebook
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,
            "type": "template",
            "template": {
                "name": message_content,
                "language": {
                    "code": "en_US"
                }
            }
        }

        try:
            # Hacer la solicitud POST a la API de Facebook
            response = requests.post(self.url, headers=headers, json=data)
            response.raise_for_status()  # Lanzar excepción si el código de respuesta no es 200-299

            # Procesar la respuesta en caso de éxito
            print("Mensaje enviado exitosamente:")
            print(json.dumps(response.json(), indent=4))

            # Actualizar el estado del mensaje en la base de datos
            message.status = "sent"
            self.message_repository.update(message)

        except requests.exceptions.HTTPError as http_err:
            # Manejo de errores HTTP
            print(f"HTTP error occurred: {http_err}")
            if response.content:
                print("Detalles del error:", response.content.decode())
            message.status = "failed"
            self.message_repository.update(message)
            raise MessageSendingException(f'HTTP error occurred: {http_err}')

        except Exception as err:
            # Manejo de errores generales
            print(f'Error inesperado: {err}')
            message.status = "failed"
            self.message_repository.update(message)
            raise MessageSendingException(f'Unexpected error: {err}')

        return message
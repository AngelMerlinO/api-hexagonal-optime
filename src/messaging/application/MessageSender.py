import os
import requests
from src.messaging.domain.Message import Message
from src.messaging.domain.MessageRepository import MessageRepository
from src.messaging.domain.exceptions import MessageSendingException

class MessageSender:
    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')  # Asegúrate de que esta variable esté correctamente configurada
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')  # Asegúrate de que esta variable esté correctamente configurada
        self.url = f'https://graph.facebook.com/v20.0/{self.phone_number_id}/messages'

    def send_whatsapp_message(self, recipient_phone_number: str, message_type: str, message_content: str) -> Message:
        message = Message(
            recipient_phone_number=recipient_phone_number,
            message_type=message_type,
            message_content=message_content,
            status="sending"
        )
        self.message_repository.save(message)

        headers = {
            'Authorization': f'Bearer {self.access_token}',  # Este token debe ser válido
            'Content-Type': 'application/json'
        }

        # Datos que se enviarán en la solicitud POST
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,  # Número de teléfono del destinatario
            "type": "template",  # Tipo de mensaje es 'template'
            "template": {
                "name": message_content,  # El nombre de la plantilla de mensaje
                "language": {
                    "code": "en_US"  # Idioma de la plantilla
                }
            }
        }

        try:
            # Realizar la solicitud POST
            response = requests.post(self.url, headers=headers, json=data)

            # Si la respuesta tiene un código de estado distinto a 200-299, generar un error
            response.raise_for_status()

            # Imprimir la respuesta para depuración
            print('Mensaje enviado exitosamente')
            print(response.json())

            # Actualizar el estado del mensaje
            message.status = "sent"
            self.message_repository.update(message)

        except requests.exceptions.HTTPError as http_err:
            # Si ocurre un error HTTP, capturarlo y registrarlo
            error_message = f'HTTP error occurred: {http_err} - {response.text}'
            print(f'Error al enviar el mensaje: {error_message}')
            message.status = "failed"
            message.error_message = error_message
            self.message_repository.update(message)
            raise MessageSendingException(error_message)

        except Exception as err:
            # Si ocurre un error general, capturarlo y registrarlo
            error_message = f'Unexpected error: {err}'
            print(f'Error inesperado: {error_message}')
            message.status = "failed"
            message.error_message = error_message
            self.message_repository.update(message)
            raise MessageSendingException(error_message)

        return message

import os
import json
import requests
from src.messaging.domain.Message import Message
from src.messaging.domain.MessageRepository import MessageRepository
from src.messaging.domain.exceptions import MessageSendingException, MessageNotFoundException

class MessageSender:
    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
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
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        data = {
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,
            "type": message_type,
            "template": {
                "name": message_content,  
                "language": {
                    "code": "en_US"
                }
            }
        }

        try:
            response = requests.post(self.url, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            print('Mensaje enviado exitosamente')
            print(json.dumps(response_data, indent=4))

            message.status = "sent"
            self.message_repository.update(message)

        except requests.exceptions.HTTPError as http_err:
            error_message = f'HTTP error occurred: {http_err} - {response.text}'
            print('Error al enviar el mensaje')
            print(f'Estatus: {response.status_code}')
            print(response.text)
            message.status = "failed"
            message.error_message = error_message
            self.message_repository.update(message)
            raise MessageSendingException(error_message)
        except Exception as err:
            error_message = f'Unexpected error: {err}'
            print(f'Error inesperado: {err}')
            message.status = "failed"
            message.error_message = error_message
            self.message_repository.update(message)
            raise MessageSendingException(error_message)

        return message
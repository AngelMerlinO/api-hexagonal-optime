import os
import requests

class WhatsAppService:
    def __init__(self):
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')  # Access token from environment variable
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')  # Phone number ID from environment variable
        self.url = f'https://graph.facebook.com/v20.0/{self.phone_number_id}/messages'

    def send_message(self, recipient_phone_number: str, template_name: str, parameters: list) -> dict:
        """
        Enviar un mensaje a través de la API de WhatsApp de Facebook con plantilla.
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # Construir el cuerpo de la solicitud para enviar un mensaje con plantilla
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": "es"
                },
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": param} for param in parameters
                        ]
                    }
                ]
            }
        }

        # Realiza la solicitud a la API de WhatsApp
        response = requests.post(self.url, headers=headers, json=data)
        response.raise_for_status()  # Lanza excepción si la solicitud falla

        return response.json()  # Devuelve la respuesta en formato JSON
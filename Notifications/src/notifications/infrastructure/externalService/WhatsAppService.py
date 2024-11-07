# Notifications/src/notifications/infrastructure/externalService/WhatsAppService.py

import os
import requests

class WhatsAppService:
    def __init__(self):
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')  # Token de acceso para la API de WhatsApp
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')  # ID del número de teléfono para la API de WhatsApp
        self.url = f'https://graph.facebook.com/v20.0/{self.phone_number_id}/messages'

    def send_message(self, recipient_phone_number: str, template_name: str, parameters: list) -> dict:
        """
        Envía un mensaje a través de la API de WhatsApp de Facebook utilizando una plantilla.
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # Construir el cuerpo de la solicitud para enviar el mensaje con plantilla
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": "es"  # Código de idioma de la plantilla
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

        # Imprimir la solicitud para depuración
        print("Sending WhatsApp message with data:", data)

        try:
            # Realiza la solicitud a la API de WhatsApp
            response = requests.post(self.url, headers=headers, json=data)
            response.raise_for_status()  # Lanza una excepción si la solicitud falla
            print("Response from WhatsApp API:", response.json())
            return response.json()  # Devuelve la respuesta en formato JSON
        except requests.exceptions.HTTPError as e:
            # Imprimir el error detallado para entender el problema
            print(f"Failed to send WhatsApp message: {e.response.status_code} - {e.response.text}")
            raise
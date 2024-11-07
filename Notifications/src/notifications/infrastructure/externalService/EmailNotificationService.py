# Notifications/src/notifications/infrastructure/EmailNotificationService.py

import requests
from src.notifications.domain.NotificationService import NotificationService

class EmailNotificationService(NotificationService):
    def send_notification(self, user_id: int, title: str, message: str):
        email_payload = {
            "email": "221255@ids.upchiapas.edu.mx",  # Cambia esto por el correo real del usuario
            "subject": title,
            "body": f"<html><body><h1>{title}</h1><p>{message}</p></body></html>"
        }
        
        lambda_url = 'https://xeaeavolvub4rybqv64adk7yhq0wajln.lambda-url.us-east-1.on.aws/'

        response = requests.post(lambda_url, json=email_payload)

        if response.status_code == 200:
            print(f"Correo enviado a {user_id}: {title} - {message}")
        else:
            print(f"Error al enviar el correo: {response.status_code} - {response.text}")
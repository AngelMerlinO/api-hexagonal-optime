import requests
from src.contact.domain.ContactNotificationService import ContactNotificationService

class HttpContactNotificationService(ContactNotificationService):
    def __init__(self, lambda_url: str):
        self.lambda_url = lambda_url

    def notify_contact_creation(self, contact_id: int, email: str):
        payload = {
            "contact_id": contact_id,
            "email": email
        }
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(self.lambda_url, json=payload, headers=headers)
        
        # Verifica si la respuesta es exitosa (código 200–299)
        if not response.ok:
            raise Exception(f"Failed to notify contact creation: {response.text}")
        
        # Verifica si el cuerpo de la respuesta contiene un mensaje de error, incluso con código 200
        response_json = response.json()
        if 'error' in response_json:
            raise Exception(f"Error in notification service: {response_json['error']}")

        return response_json
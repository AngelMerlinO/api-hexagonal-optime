# Notifications/src/notifications/infrastructure/WhatsAppNotificationService.py

from src.notifications.domain.NotificationService import NotificationService
from src.notifications.infrastructure.externalService.WhatsAppService import WhatsAppService

class WhatsAppNotificationService(NotificationService):
    def __init__(self):
        # Instancia de WhatsAppService
        self.whatsapp_service = WhatsAppService()
        
    def send_notification(self, user_id: int, title: str, message: str):
        # Definir el número de teléfono del destinatario
        recipient_phone_number = "529515271070"  # Asegúrate de que el formato del número sea correcto

        # Nombre de la plantilla de WhatsApp
        template_name = "generic_notification"  # Usa "generic_notification" si está aprobada

        # Parámetros que se inyectarán en la plantilla
        parameters = [title, message]

        # Enviar el mensaje usando WhatsAppService
        try:
            response = self.whatsapp_service.send_message(
                recipient_phone_number=recipient_phone_number,
                template_name=template_name,
                parameters=parameters
            )
            print("WhatsApp message sent successfully:", response)
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")
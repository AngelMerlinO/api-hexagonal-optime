from src.messaging.domain.Message import Message
from src.messaging.domain.MessageRepository import MessageRepository
from src.messaging.domain.exceptions import MessageSendingException
from src.messaging.infrastructure.WhatsAppService import WhatsAppService  # Importamos el servicio

class MessageSender:
    def __init__(self, message_repository: MessageRepository, whatsapp_service: WhatsAppService):
        self.message_repository = message_repository
        self.whatsapp_service = whatsapp_service  # Inyectamos el servicio de WhatsApp

    def send_payment_confirmation(self, recipient_phone_number: str, status: str, amount: str, currency: str, payment_id: str) -> Message:
        # Crear el objeto de mensaje
        message = Message(
            recipient_phone_number=recipient_phone_number,
            message_type="template",
            message_content="confirmacion_pago",
            status="sending"
        )
        self.message_repository.save(message)

        try:
            # Parámetros de la plantilla
            parameters = [status, amount, currency, payment_id]

            # Llamar al servicio de WhatsApp para enviar el mensaje
            response = self.whatsapp_service.send_message(recipient_phone_number, "confirmacion_pago", parameters)

            # Procesar la respuesta en caso de éxito
            print("Mensaje enviado exitosamente:")
            print(response)

            # Actualizar el estado del mensaje en la base de datos
            message.status = "sent"
            self.message_repository.update(message)

        except Exception as err:
            # Manejo de errores generales
            print(f'Error al enviar mensaje: {err}')
            message.status = "failed"
            self.message_repository.update(message)
            raise MessageSendingException(f'Error sending message: {err}')

        return message
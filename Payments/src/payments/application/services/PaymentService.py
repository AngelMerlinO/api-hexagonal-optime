from src.payments.domain.PaymentRepository import PaymentRepository
from src.payments.domain.Payment import Payment
from src.payments.domain.exceptions import PaymentProcessingException, PaymentNotFoundException
from src.payments.infrastructure.MercadoPagoService import MercadoPagoService
from src.payments.domain.EventPublisher import EventPublisher
import os

class PaymentService:
    def __init__(self, payment_repository: PaymentRepository, mercado_pago_service: MercadoPagoService, publisher: EventPublisher):
        self.payment_repository = payment_repository
        self.mercado_pago_service = mercado_pago_service
        self.publisher = publisher

    def create_payment(self, user_id: int, items: list, payer: dict, description: str = None):
        # Calcula el monto total y la moneda
        amount = sum(item['unit_price'] * item['quantity'] for item in items)
        currency_id = items[0]['currency_id'] if items else 'MXN'

        # Crea el registro de pago inicial en la base de datos con preference_id vacío
        payment = Payment(
            user_id=user_id,
            preference_id='',
            amount=amount,
            currency_id=currency_id,
            description=description
        )
        self.payment_repository.save(payment)  # Guarda el pago inicial sin preference_id

        # Genera la preferencia en Mercado Pago
        base_url = os.getenv('BASE_URL')
        preference_data = {
            "items": items,
            "payer": payer,
            "external_reference": str(payment.id),
            "metadata": {"payment_id": str(payment.id)},
            "notification_url": f"{base_url}/api/v1/payments/notifications",
            "back_urls": {
                "success": f"{base_url}/api/v1/payments/retorno",
                "failure": f"{base_url}/api/v1/payments/retorno",
                "pending": f"{base_url}/api/v1/payments/retorno"
            },
            "auto_return": "approved"
        }

        try:
            # Llama al servicio de Mercado Pago y obtiene el `preference_id`
            preference = self.mercado_pago_service.create_preference(preference_data)
            payment.preference_id = preference.get("id")
            
            # Actualiza el pago en el repositorio con el `preference_id`
            self.payment_repository.update(payment)

            return {
                "init_point": preference["init_point"],
                "preference_id": preference["id"]
            }

        except Exception as e:
            raise PaymentProcessingException(f"Error creating payment: {str(e)}")
        
    def process_notification(self, data: dict):
        topic = data.get("topic") or data.get("type")
        payment_id = data.get('data', {}).get('id')

        if topic == "payment" and payment_id:
            # Obtén los datos del pago desde Mercado Pago
            payment_data = self.mercado_pago_service.get_payment_data(payment_id)

            # Busca el pago en la base de datos usando `external_reference` (ID del pago local)
            payment = self.payment_repository.find_by_id(int(payment_data.get("external_reference")))
            if not payment:
                raise PaymentNotFoundException("Payment not found in database")

            # Actualiza los detalles del pago con la información recibida en la notificación
            payment.payment_id = payment_data.get("id")
            payment.status = payment_data.get("status")
            payment.status_detail = payment_data.get("status_detail")
            payment.date_created = payment_data.get("date_created")
            payment.currency_id = payment_data.get("currency_id")

            # Guarda los cambios en el repositorio
            self.payment_repository.update(payment)

            # Publica en la cola de RabbitMQ con los datos actualizados del pago
            self._publish_payment_update(payment)

            return payment
        else:
            return {"status": "ignored"}

    def get_payment_status(self, payment_id: str):
        # Busca el estado del pago en la base de datos
        payment = self.payment_repository.find_by_payment_id(payment_id)
        if not payment:
            # Si no se encuentra, busca la información directamente en Mercado Pago
            payment_data = self.mercado_pago_service.get_payment_data(payment_id)
            payment = Payment(
                user_id=1,
                preference_id=payment_data.get('preference_id'),
                payment_id=payment_data.get('id'),
                amount=payment_data.get('transaction_amount'),
                currency_id=payment_data.get('currency_id'),
                description=payment_data.get('description'),
                status=payment_data.get('status'),
                status_detail=payment_data.get('status_detail'),
                date_created=payment_data.get('date_created')
            )
            self.payment_repository.save(payment)
        return payment

    def _publish_payment_update(self, payment: Payment):
        """Publica un mensaje a la cola de RabbitMQ con los detalles del pago solo cuando los datos clave están completos."""
        # Construye el mensaje solo con los datos completos, convirtiendo `Decimal` a `float`
        event_data = {
            "user_id": payment.user_id,
            "title": "Pago actualizado",
            "message": f"Actualización del estado del pago con ID {payment.payment_id}: {payment.status_detail} con valor de {payment.amount}.",
            "type": "email",  # Tipo de notificación, puedes modificar según sea necesario
            "service_type": "email",  # Cambiar según el tipo de servicio que necesites (email o whatsapp)
            "link": f"https://example.com/payments/{payment.payment_id}",  # Enlace de referencia
            "payment_details": {  # Detalles específicos del pago
                "payment_id": payment.payment_id,
                "status": payment.status,
                "amount": float(payment.amount),
                "currency_id": payment.currency_id,
                "preference_id": payment.preference_id
            }
        }
        
        # Publica el mensaje solo si los datos clave están completos y no son `None`
        if payment.payment_id and payment.status and payment.status_detail:
            print("Intentando publicar en RabbitMQ:", event_data)  # Debug log
            try:
                self.publisher.publish(event_data, routing_key='payment.created')
                print("Publicación en RabbitMQ exitosa.")
            except Exception as e:
                print(f"Error publicando en RabbitMQ: {e}")
        else:
            print("Datos incompletos; publicación en RabbitMQ omitida:", event_data)
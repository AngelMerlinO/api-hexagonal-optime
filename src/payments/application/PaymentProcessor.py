import os
import mercadopago
import time
from src.payments.domain.PaymentRepository import PaymentRepository
from src.users.domain.UserRepository import UserRepository
from src.payments.domain.Payment import Payment
from src.payments.domain.exceptions import PaymentProcessingException, PaymentNotFoundException
from src.users.domain.exceptions import UserNotFoundException

class PaymentProcessor:
    def __init__(self, payment_repository: PaymentRepository, user_repository: UserRepository):
        self.payment_repository = payment_repository
        self.user_repository = user_repository
        self.sdk = mercadopago.SDK(os.getenv('MERCADOPAGO_ACCESS_TOKEN'))

    def create_payment(self, user_id: int, items: list, payer: dict, description: str = None):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} does not exist")

        # Crear el registro de pago en la base de datos (sin 'preference_id' aún)
        amount = sum(item['unit_price'] * item['quantity'] for item in items)
        currency_id = items[0]['currency_id'] if items else 'MXN'

        # Crear el pago en la base de datos
        payment = Payment(
            user_id=user_id,
            preference_id='',  # Será actualizado después
            amount=amount,
            currency_id=currency_id,
            description=description
        )
        self.payment_repository.save(payment)

        # Crear la preferencia de pago en MercadoPago
        base_url = os.getenv('BASE_URL')

        preference_data = {
            "items": items,
            "payer": payer,
            "external_reference": str(payment.id),
            "metadata": {
                "payment_id": str(payment.id)
            },
            "notification_url": f"{base_url}/api/v1/payments/notifications",  # URL pública para recibir notificaciones
            "back_urls": {
                "success": f"{base_url}/api/v1/payments/retorno",
                "failure": f"{base_url}/api/v1/payments/retorno",
                "pending": f"{base_url}/api/v1/payments/retorno"
            },
            "auto_return": "approved"
        }

        print("Preference Data:", preference_data)  # Para depuración

        try:
            # Crear preferencia en MercadoPago
            preference_response = self.sdk.preference().create(preference_data)
            preference = preference_response["response"]

            # Actualizar el registro de pago en la base de datos con el preference_id
            payment.preference_id = preference['id']
            self.payment_repository.update(payment)

            return {
                "init_point": preference["init_point"],
                "preference_id": preference["id"]
            }

        except Exception as e:
            raise PaymentProcessingException(f"Error creating payment: {str(e)}")

    def process_notification(self, data: dict):
        print(f"Notification data received: {data}")
        topic = data.get("topic") or data.get("type")
        payment_id = None

        if 'data' in data and 'id' in data['data']:
            payment_id = data['data']['id']
        elif 'id' in data:
            payment_id = data['id']
        else:
            payment_id = data.get('id') or data.get('data.id') or data.get('data', {}).get('id')

        if topic == "payment" and payment_id:
            # Intentar obtener la información del pago desde MercadoPago
            payment_data = None
            max_retries = 5
            retry_delay = 2  # segundos

            for attempt in range(max_retries):
                try:
                    payment_response = self.sdk.payment().get(payment_id)
                    payment_data = payment_response.get("response")
                    if payment_data and payment_data.get("status"):
                        break
                except Exception as e:
                    print(f"Error obteniendo payment_data en el intento {attempt + 1}: {str(e)}")
                time.sleep(retry_delay)

            if not payment_data:
                raise PaymentProcessingException("Unable to retrieve payment data after retries")

            print("Payment Data:", payment_data)  # Para depuración

            # Extraer los datos necesarios
            payment_id = str(payment_data.get("id"))
            status = payment_data.get("status")
            status_detail = payment_data.get("status_detail")
            date_created = payment_data.get("date_created")
            external_reference = payment_data.get("external_reference")

            # Intentar obtener el pago en la base de datos usando la referencia externa
            payment = self.payment_repository.find_by_id(int(external_reference))

            if not payment:
                raise PaymentNotFoundException("Payment not found in database")

            # Actualizar el pago con los detalles obtenidos
            payment.payment_id = payment_id
            payment.status = status
            payment.status_detail = status_detail
            payment.date_created = date_created

            self.payment_repository.update(payment)

            print(f"Payment {payment_id} updated to status {status} ({status_detail})")
            return payment

        else:
            print(f"Ignoring notification of type {topic}")
            return {"status": "ignored"}
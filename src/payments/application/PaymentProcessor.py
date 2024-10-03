# src/payments/application/PaymentProcessor.py

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
        # Inicializa el SDK de MercadoPago con el Access Token desde variables de entorno
        self.sdk = mercadopago.SDK(os.getenv('MERCADOPAGO_ACCESS_TOKEN'))

    def create_payment(self, user_id: int, items: list, payer: dict, description: str = None):
        # Verificar si el usuario existe
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

        # Crear la preferencia de pago con metadata
        base_url = os.getenv('BASE_URL')

        preference_data = {
            "items": items,
            "payer": payer,
            "external_reference": str(payment.id),
            "metadata": {
                "payment_id": str(payment.id)
            },
            "notification_url": f"{base_url}/payments/notifications",
            "back_urls": {
                "success": f"{base_url}/payments/retorno",
                "failure": f"{base_url}/payments/retorno",
                "pending": f"{base_url}/payments/retorno"
            },
            "auto_return": "approved"
        }

        # Registrar preference_data para depuración
        print("Preference Data:", preference_data)

        try:
            preference_response = self.sdk.preference().create(preference_data)
            preference = preference_response["response"]

            # Actualizar el registro de pago con el 'preference_id'
            payment.preference_id = preference['id']
            self.payment_repository.update(payment)

            return {
                "init_point": preference["init_point"],
                "preference_id": preference["id"]
            }

        except Exception as e:
            raise PaymentProcessingException(f"Error creating payment: {str(e)}")

    def process_notification(self, data: dict):
        print("Iniciando process_notification")
        print(f"Datos de notificación: {data}")
        topic = data.get("topic") or data.get("type")
        payment_id = None

        # Extracción correcta del payment_id
        if 'data' in data and 'id' in data['data']:
            payment_id = data['data']['id']
        elif 'id' in data:
            payment_id = data['id']
        else:
            payment_id = data.get('id') or data.get('data.id') or data.get('data', {}).get('id')

        if topic == "payment" and payment_id:
            # Intentar obtener la información completa del pago, con reintentos
            max_retries = 5
            retry_delay = 2  # segundos
            payment_data = None

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

            # Registrar payment_data para depuración
            print("Payment Data:", payment_data)

            # Extraer los datos necesarios
            payment_id = str(payment_data.get("id"))
            status = payment_data.get("status")
            status_detail = payment_data.get("status_detail")
            date_created = payment_data.get("date_created")
            external_reference = payment_data.get("external_reference")
            metadata = payment_data.get("metadata", {})

            # Intentar obtener payment_id desde metadata si external_reference es None
            if not external_reference:
                payment_id_in_metadata = metadata.get("payment_id")
                if not payment_id_in_metadata:
                    raise PaymentProcessingException("payment_id not found in payment metadata")
                # Buscar el pago en la base de datos usando payment_id_in_metadata
                payment = self.payment_repository.find_by_id(int(payment_id_in_metadata))
            else:
                # Buscar el pago en la base de datos usando external_reference
                payment = self.payment_repository.find_by_id(int(external_reference))

            if not payment:
                raise PaymentNotFoundException("Payment not found in database")

            # Actualizar los campos del pago
            payment.payment_id = payment_id
            payment.status = status
            payment.status_detail = status_detail
            payment.date_created = date_created

            self.payment_repository.update(payment)

            print(f"Actualizando pago {payment_id} a estado {status} ({status_detail})")

            return payment

        else:
            # Ignorar otros tipos de notificaciones
            print(f"Ignorando notificación de tipo {topic}")
            return {"status": "ignored"}

    def process_notification(self, data: dict):
        print("Iniciando process_notification")
        print(f"Datos de notificación: {data}")
        topic = data.get("topic") or data.get("type")
        payment_id = None

        if 'data' in data and 'id' in data['data']:
            payment_id = data['data']['id']
        elif 'id' in data:
            payment_id = data['id']
        else:
            payment_id = data.get('id') or data.get('data.id') or data.get('data', {}).get('id')

        if topic == "payment" and payment_id:
            # Intentar obtener la información completa del pago, con reintentos
            max_retries = 5
            retry_delay = 2  # segundos
            payment_data = None

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

            # Registrar payment_data para depuración
            print("Payment Data:", payment_data)

            # Extraer los datos necesarios
            payment_id = str(payment_data.get("id"))
            status = payment_data.get("status")
            status_detail = payment_data.get("status_detail")
            date_created = payment_data.get("date_created")
            external_reference = payment_data.get("external_reference")

            # Intentar obtener payment_id desde metadata si external_reference es None
            if not external_reference:
                metadata = payment_data.get("metadata", {})
                payment_id_in_metadata = metadata.get("payment_id")

                if not payment_id_in_metadata:
                    raise PaymentProcessingException("payment_id not found in payment metadata")

                # Buscar el pago en la base de datos usando payment_id_in_metadata
                payment = self.payment_repository.find_by_id(int(payment_id_in_metadata))
            else:
                # Buscar el pago en la base de datos usando external_reference
                payment = self.payment_repository.find_by_id(int(external_reference))

            if not payment:
                raise PaymentNotFoundException("Payment not found in database")

            # Actualizar los campos del pago
            payment.payment_id = payment_id
            payment.status = status
            payment.status_detail = status_detail
            payment.date_created = date_created

            self.payment_repository.update(payment)

            print(f"Actualizando pago {payment_id} a estado {status} ({status_detail})")

            return payment

        else:
            # Ignorar otros tipos de notificaciones
            print(f"Ignorando notificación de tipo {topic}")
            return {"status": "ignored"}

    def get_payment_status(self, payment_id: str):
        payment = self.payment_repository.find_by_payment_id(payment_id)
        if not payment:
            # Intentar obtener los datos desde MercadoPago
            payment_response = self.sdk.payment().get(payment_id)
            payment_data = payment_response["response"]

            # Extraer los datos necesarios
            payment_id = str(payment_data.get("id"))
            status = payment_data.get("status")
            status_detail = payment_data.get("status_detail")
            date_created = payment_data.get("date_created")
            amount = payment_data.get('transaction_amount')
            currency_id = payment_data.get('currency_id')
            description = payment_data.get('description')
            external_reference = payment_data.get("external_reference")
            user_id = self.get_user_id_from_payment_data(payment_data)

            # Crear un nuevo registro en la base de datos
            payment = Payment(
                user_id=user_id,
                preference_id=payment_data.get('preference_id', ''),
                payment_id=payment_id,
                amount=amount,
                currency_id=currency_id,
                description=description,
                status=status,
                status_detail=status_detail,
                date_created=date_created
            )
            self.payment_repository.save(payment)
        else:
            # Devolver el pago existente
            pass

        return payment

    def get_user_id_from_payment_data(self, payment_data):
        # Intentar obtener el user_id desde el campo 'external_reference'
        external_reference = payment_data.get('external_reference')
        if external_reference:
            return int(external_reference)
        else:
            # Si no está disponible, manejar el caso
            raise PaymentProcessingException("User ID not found in payment data")
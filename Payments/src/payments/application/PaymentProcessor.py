from src.payments.domain.PaymentRepository import PaymentRepository
from src.payments.domain.Payment import Payment
from src.payments.domain.exceptions import PaymentProcessingException, PaymentNotFoundException
from src.payments.infrastructure.MercadoPagoService import MercadoPagoService
import os

class PaymentProcessor:
    def __init__(self, payment_repository: PaymentRepository, mercado_pago_service: MercadoPagoService):
        self.payment_repository = payment_repository
        self.mercado_pago_service = mercado_pago_service

    def create_payment(self, user_id: int, items: list, payer: dict, description: str = None):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            ### CAMBIAR EXEPCION A EL CORRESPONDIENTE   ###
            raise PaymentNotFoundException(f"User with id {user_id} does not exist")

        amount = sum(item['unit_price'] * item['quantity'] for item in items)
        currency_id = items[0]['currency_id'] if items else 'MXN'

        payment = Payment(
            user_id=user_id,
            preference_id='',
            amount=amount,
            currency_id=currency_id,
            description=description
        )
        self.payment_repository.save(payment)

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
            preference = self.mercado_pago_service.create_preference(preference_data)
            payment.preference_id = preference['id']
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
            payment_data = self.mercado_pago_service.get_payment_data(payment_id)

            payment = self.payment_repository.find_by_id(int(payment_data.get("external_reference")))
            if not payment:
                raise PaymentNotFoundException("Payment not found in database")

            payment.payment_id = payment_data.get("id")
            payment.status = payment_data.get("status")
            payment.status_detail = payment_data.get("status_detail")
            payment.date_created = payment_data.get("date_created")
            payment.currency_id = payment_data.get("currency_id")

            self.payment_repository.update(payment)
            return payment
        else:
            return {"status": "ignored"}

    def get_payment_status(self, payment_id: str):
        payment = self.payment_repository.find_by_payment_id(payment_id)
        if not payment:
            payment_data = self.mercado_pago_service.get_payment_data(payment_id)
            payment = Payment(
                user_id=1,  # You need to extract the real user_id from the payment_data if necessary
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
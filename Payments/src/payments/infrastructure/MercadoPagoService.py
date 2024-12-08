import os
import mercadopago

class MercadoPagoService:
    def __init__(self):
        self.sdk = mercadopago.SDK(os.getenv('MERCADOPAGO_ACCESS_TOKEN'))

    def create_preference(self, preference_data: dict):
        try:
            preference_response = self.sdk.preference().create(preference_data)
           
            return preference_response["response"]
        except Exception as e:
            raise Exception(f"Error creating MercadoPago preference: {str(e)}")

    def get_payment_data(self, payment_id: str):
        try:
            payment_response = self.sdk.payment().get(payment_id)
            return payment_response.get("response")
        except Exception as e:
            raise Exception(f"Error getting MercadoPago payment data: {str(e)}")
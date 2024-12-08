class PaymentEventHandler:
    def handle_payment_created_event(self, message: dict):
        payment_id = message.get("payment_id")
        
        
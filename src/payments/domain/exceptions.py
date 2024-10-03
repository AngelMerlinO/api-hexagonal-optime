# src/payments/domain/exceptions.py

class PaymentNotFoundException(Exception):
    pass

class PaymentProcessingException(Exception):
    pass
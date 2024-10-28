class ContactAlreadyExistsException(Exception):
    pass

class InvalidContactDataException(Exception):
    pass

class ContactNotFoundException(Exception):
    """Excepción lanzada cuando no se encuentra un contacto."""
    pass
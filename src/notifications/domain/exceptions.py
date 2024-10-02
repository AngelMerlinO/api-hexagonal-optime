# src/notifications/domain/exceptions.py

class NotificationNotFoundException(Exception):
    pass

class InvalidNotificationTypeException(Exception):
    pass

class InvalidNotificationStatusException(Exception):
    pass
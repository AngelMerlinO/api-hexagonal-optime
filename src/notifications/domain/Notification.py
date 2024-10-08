import enum

class NotificationType(enum.Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'
    in_app = 'in-app'

class NotificationStatus(enum.Enum):
    sent = 'sent'
    pending = 'pending'
    failed = 'failed'

class Notification:
    def __init__(self, user_id, title, message, type: NotificationType, link=None):
        self.user_id = user_id
        self.title = title
        self.message = message
        self.type = type
        self.link = link

    def __repr__(self):
        return f"<Notification {self.title} to User {self.user_id}>"
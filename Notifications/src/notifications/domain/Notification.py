import enum
from datetime import datetime, timezone
from typing import Optional

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
    def __init__(self, user_id, title, message, type: NotificationType, status: NotificationStatus = NotificationStatus.pending, link=None, id=None, uuid=None, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None, deleted_at: Optional[datetime] = None):
        self.user_id = user_id
        self.uuid = uuid
        self.title = title
        self.message = message
        self.type = type
        self.status = status
        self.link = link
        self.id = id
        self.created_at = created_at or datetime.now().astimezone()
        self.updated_at = updated_at or datetime.now().astimezone()
        self.deleted_at = deleted_at

    def __repr__(self):
        return f"<Notification {self.title} to User {self.user_id}>"

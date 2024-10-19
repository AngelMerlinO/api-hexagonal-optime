from datetime import date
from enum import Enum

class ActivityType(Enum):
    exam = 'exam'
    assignment = 'assignment'
    project = 'project'
    quiz = 'quiz'

class ActivityStatus(Enum):
    sent = 'sent'
    pending = 'pending'
    completed = 'completed'
    overdue = 'overdue'

class Activities:
    def __init__(self, user_id: int, title: str, description: str, activity_type: ActivityType, status: ActivityStatus, delivery_date: date, link_classroom: str = None, uuid: str = None, id: int = None):
        self.id = id
        self.uuid = uuid
        self.user_id = user_id
        self.title = title
        self.description = description
        self.type = activity_type
        self.status = status
        self.delivery_date = delivery_date
        self.link_classroom = link_classroom

    def __repr__(self):
        return f"<Activities {self.title} for User {self.user_id}>"
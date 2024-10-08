import enum
from datetime import date

# Definir los tipos de actividades como un enum
class ActivityType(enum.Enum):
    exam = 'exam'
    assignment = 'assignment'
    project = 'project'
    quiz = 'quiz'

# Definir los posibles estados de las actividades como un enum
class ActivityStatus(enum.Enum):
    sent = 'sent'
    pending = 'pending'
    completed = 'completed'
    overdue = 'overdue'

class Activities:
    def __init__(self, user_id: int, title: str, description: str, activity_type: ActivityType, delivery_date: date, link_classroom: str, status: ActivityStatus):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.type = activity_type
        self.delivery_date = delivery_date
        self.link_classroom = link_classroom
        self.status = status

    def __repr__(self):
        return f"<Activity {self.title} for User {self.user_id}>"
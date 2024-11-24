from typing import Optional, List
from src.subject.domain.subject import Subject

class Schedule:
    def __init__(self, user_id: int, items: Optional[List[Subject]] = None, uuid: str = None):
        self.user_id = user_id
        self.items = items or []
        self.uuid = uuid
        
    def __repr__(self):
        return f"<Schedule id {self.id} for User {self.user_id}>"
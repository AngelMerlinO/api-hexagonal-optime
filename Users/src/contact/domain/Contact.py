from typing import Optional
from datetime import datetime

class Contact:
    def __init__(self, id: Optional[int], email: str, phone: str, name: str, last_name:str ,created_at: Optional[datetime] = None, 
                 updated_at: Optional[datetime] = None, deleted_at: Optional[datetime] = None):
        self.id = id
        self.email = email
        self.phone = phone
        self.name = name
        self.last_name = last_name
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.deleted_at = deleted_at
        
    def __repr__(self) -> str:
        return f"<Contact {self.email} for User {self.phone}>"

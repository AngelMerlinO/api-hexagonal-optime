from typing import Optional
from datetime import datetime

class Contact:
    def __init__(self, id: Optional[int], email: str, phone: str, created_at: Optional[datetime] = None, 
                 updated_at: Optional[datetime] = None, deleted_at: Optional[datetime] = None):
        self.id = id
        self.email = email
        self.phone = phone
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.deleted_at = deleted_at
    
    def soft_delete(self):
        """Marca el contacto como eliminado (soft delete)"""
        self.deleted_at = datetime.now()
    
    def is_deleted(self) -> bool:
        """Retorna True si el contacto ha sido eliminado lógicamente"""
        return self.deleted_at is not None
    
    def __repr__(self):
        return f"<Contact {self.email} for User {self.phone}>"
from src.users.domain.UserRepository import UserRepository
from src.users.domain.User import User
from sqlalchemy.orm import Session

class MySqlUserRepository(UserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, user: User):
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)  # Actualiza el ID del usuario después de guardarlo
        return user

    def update(self, user: User):
        self.db_session.merge(user)  # SQLAlchemy maneja las actualizaciones
        self.db_session.commit()

    def find_by_id(self, user_id: int) -> User:
        user = self.db_session.query(User).filter_by(id=user_id).first()
        if not user:
            raise Exception(f"User with id {user_id} not found")
        return user
    
    def delete(self, user: User):
        if not user:
            raise Exception(f"User with id {user.id} not found")
        
        self.db_session.delete(user)
        self.db_session.commit()
        
        return f"User with id {user.id} eliminated successfully."
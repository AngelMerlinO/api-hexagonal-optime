from sqlalchemy.orm import Session
from src.users.domain.UserRepository import UserRepository
from src.users.infrastructure.orm.UserModel import UserModel
from src.users.domain.User import User

class MySqlUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User):
        user_model = UserModel(username=user.username, email=user.email, password=user.password)
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)
        
        user.id = user_model.id
        print(user_model.id, "Este es el id del usuario")

    def update(self, user: User):
        user_model = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if user_model:
            user_model.username = user.username
            user_model.email = user.email
            user_model.password = user.password
            self.db.commit()
        else:
            raise ValueError(f"User with ID {user.id} not found")

    def find_by_id(self, user_id: int) -> User:
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            raise ValueError(f"User with ID {user_id} not found")
        return User(id=user_model.id ,username=user_model.username, email=user_model.email, password=user_model.password)

    def delete(self, user: User):
        user_model = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if user_model:
            self.db.delete(user_model)
            self.db.commit()
        else:
            raise ValueError(f"User with ID {user.id} not found")
from sqlalchemy.orm import Session
from src.users.domain.UserRepository import UserRepository
from src.users.infrastructure.orm.UserModel import UserModel
from src.users.domain.User import User
from typing import Optional


class MySqlUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User):
        user_model = UserModel(
            uuid=user.uuid,
            contact_id=user.contact_id,
            username=user.username,
            email=user.email,
            password=user.password
        )
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)

        user.id = user_model.id
        print(user_model.id, "Este es el id del usuario")

    def update_by_id(self, id: int, username: Optional[str], email: Optional[str], password: Optional[str]):
        user_model = self.db.query(UserModel).filter(UserModel.id == id).first()
        if not user_model:
            raise ValueError(f"User with ID {id} not found")

        if username:
            user_model.username = username
        if email:
            user_model.email = email
        if password:
            user_model.password = password

        self.db.commit()
        return user_model

    def update_by_uuid(self, uuid: str, username: Optional[str], email: Optional[str], password: Optional[str]):
        user_model = self.db.query(UserModel).filter(UserModel.uuid == uuid).first()
        if not user_model:
            raise ValueError(f"User with UUID {uuid} not found")

        self._update_user_fields(user_model, username, email, password)
        self.db.commit()
        return user_model

    def find_by_id(self, id: int) -> User:
        user_model = self.db.query(UserModel).filter(UserModel.id == id).first()
        if not user_model:
            raise ValueError(f"User with ID {id} not found")
        return user_model

    def find_by_uuid(self, uuid: str) -> User:
        user_model = self.db.query(UserModel).filter(UserModel.uuid == uuid).first()
        if not user_model:
            raise ValueError(f"User with UUID {uuid} not found")
        return user_model

    def delete_by_id(self, id: int):
        user_model = self.db.query(UserModel).filter(UserModel.id == id).first()
        if not user_model:
            raise ValueError(f"User with ID {id} not found")

        self.db.delete(user_model)
        self.db.commit()

    def delete_by_uuid(self, uuid: str):
        user_model = self.db.query(UserModel).filter(UserModel.uuid == uuid).first()
        if not user_model:
            raise ValueError(f"User with UUID {uuid} not found")

        self.db.delete(user_model)
        self.db.commit()

    def _update_user_fields(self, user_model: UserModel, username: Optional[str], email: Optional[str], password: Optional[str]):
        if username:
            user_model.username = username
        if email:
            user_model.email = email
        if password:
            user_model.password = password

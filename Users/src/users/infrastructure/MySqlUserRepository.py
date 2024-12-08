from sqlalchemy.orm import Session
from src.users.domain.UserRepository import UserRepository
from src.users.infrastructure.orm.UserModel import UserModel
from src.contact.infraestructure.orm.ContactModel import ContactModel
from src.users.domain.User import User
from typing import Optional
from datetime import datetime


class MySqlUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User):
        
        current_time = datetime.now()
        
        user_model = UserModel(
            uuid=user.uuid,
            contact_id=user.contact_id,
            username=user.username,
            password=user.password,
            verify_at=current_time
        )
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)

        user.id = user_model.id
        print(user_model.id)
        
        return user_model.id
        
    def find_by_username(self, username: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def update_by_id(self, id: int, username: Optional[str], password: Optional[str]):
        user_model = self.db.query(UserModel).filter(UserModel.id == id).first()
        if not user_model:
            raise ValueError(f"User with ID {id} not found")

        if username:
            user_model.username = username
        if password:
            user_model.password = password

        self.db.commit()
        return user_model

    def update_by_uuid(self, uuid: str, username: Optional[str], password: Optional[str]):
        user_model = self.db.query(UserModel).filter(UserModel.uuid == uuid).first()
        if not user_model:
            raise ValueError(f"User with UUID {uuid} not found")

        self._update_user_fields(user_model, username, password)
        self.db.commit()
        return user_model

    def find_by_id(self, id: int) -> dict:
        user_model = (
            self.db.query(UserModel)
            .filter(UserModel.id == id)
            .outerjoin(ContactModel, UserModel.contact_id == ContactModel.id)
            .first()
        )
        
        if not user_model:
            raise ValueError(f"User with ID {id} not found")

        # Construir el objeto User con datos del Contact o un contacto vacío
        contact = {
            "id": user_model.contacts.id if user_model.contacts else None,
            "email": user_model.contacts.email if user_model.contacts else None,
            "phone": user_model.contacts.phone if user_model.contacts else None
        } if user_model.contacts else {}

        return {
            "id": user_model.id,
            "username": user_model.username,
            "password": user_model.password,
            "uuid": user_model.uuid,
            "contact": contact
        }

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

    def _update_user_fields(self, user_model: UserModel, username: Optional[str], password: Optional[str]):
        if username:
            user_model.username = username
        if password:
            user_model.password = password

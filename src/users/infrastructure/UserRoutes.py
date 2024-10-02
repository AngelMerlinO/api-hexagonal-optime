from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.users.application.UserCreator import UserCreator
from src.users.application.UserUpdater import UserUpdater
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from config.database import get_db
from pydantic import BaseModel

# Crear el router específico para usuarios
router = APIRouter()

# Modelo Pydantic para crear y actualizar usuarios
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    password: str = None

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    repo = MySqlUserRepository(db)
    user_creator = UserCreator(repo)
    try:
        user_creator.create(user.username, user.email, user.password)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    repo = MySqlUserRepository(db)
    user_updater = UserUpdater(repo)
    try:
        user_updater.update(user_id, user.username, user.email, user.password)
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
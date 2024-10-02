from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.users.application.UserCreator import UserCreator
from src.users.application.UserUpdater import UserUpdater
from src.users.application.UserEliminator import UserEliminator
from src.users.application.UserFindById import UserFindById
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
    
@router.get("/users/{user_id}")
def find_by_id(user_id: int, db: Session = Depends(get_db)):
    repo = MySqlUserRepository(db)
    user_finder = UserFindById(repo)
    try:
        user = user_finder.find_by_id(user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error finding user")
    
    
    
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
    
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    repo = MySqlUserRepository(db)
    user_eliminator = UserEliminator(repo)
    try:
        user_eliminator.delete(user_id)
        return {"message": f"User with ID {user_id} eliminated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
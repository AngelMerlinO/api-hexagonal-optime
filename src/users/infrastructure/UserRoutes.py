from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.users.application.UserCreator import UserCreator
from src.users.application.UserUpdater import UserUpdater
from src.users.application.UserEliminator import UserEliminator
from src.users.application.UserFindById import UserFindById
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from src.contact.infraestructure.MySqlContactRepository import MySqlContactRepository
from slowapi import Limiter
from slowapi.util import get_remote_address
from config.database import get_db
from pydantic import BaseModel
from fastapi import Query

limiter = Limiter(key_func=get_remote_address)


router = APIRouter(
    prefix=("/api/v1/users"),
    tags=['users']
)

class UserCreate(BaseModel):
    contact_id: int
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    password: str = None

@router.get("/{user_id}")
@limiter.limit("5/minute")  # Limitar a 5 peticiones por minuto
def find_user_by_id(user_id: int, request: Request, db: Session = Depends(get_db)):
    repo = MySqlUserRepository(db)
    try:
        user = repo.find_by_id(user_id)
        if user is None:  # Asegúrate de que el repositorio maneje esto
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error finding user by ID")

@router.post("/")
@limiter.limit("2/minute")  
def create_user(user: UserCreate,request:Request, db: Session = Depends(get_db)):
    repo = MySqlUserRepository(db)
    contact_repo = MySqlContactRepository(db)
    user_creator = UserCreator(repo, contact_repo)
    try:
        user_creator.create(user.contact_id,user.username, user.email, user.password)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}")
@limiter.limit("2/minute")  
def update_user_by_id(user_id: int, request:Request, user: UserUpdate, db: Session = Depends(get_db)):
    repo = MySqlUserRepository(db)
    try:
        repo.update_by_id(
            id=user_id,
            username=user.username,
            email=user.email,
            password=user.password
        )
        return {"message": "User updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
@limiter.limit("1/minute")  
def delete_user_by_id(user_id: int, request:Request, db: Session = Depends(get_db)):
    repo = MySqlUserRepository(db)
    try:
        repo.delete_by_id(user_id)
        return {"message": f"User with ID {user_id} eliminated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

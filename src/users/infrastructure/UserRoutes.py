from fastapi import APIRouter, Depends, HTTPException, Request, Query 
from sqlalchemy.orm import Session
from src.users.application.UserCreator import UserCreator
from src.users.application.UserUpdater import UserUpdater
from src.users.application.UserEliminator import UserEliminator
from src.users.application.UserFindById import UserFindById
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from src.contact.infraestructure.MySqlContactRepository import MySqlContactRepository
from src.auth.jwt_handler import create_access_token
from src.auth.jwt_handler import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.auth.jwt_handler import create_access_token
from src.auth.jwt_handler import get_current_user
from config.database import get_db
from pydantic import BaseModel, EmailStr, constr, validator


limiter = Limiter(key_func=get_remote_address)


router = APIRouter(
    prefix=("/api/v1/users"),
    tags=['users']
)

class UserCreate(BaseModel):
    contact_id: int
    username: str
    email: EmailStr
    password: constr(min_length=8, max_length=16)  # type: ignore # Restricción de longitud para contraseñas

    @validator('password')
    def no_spaces_in_password(cls, value):
        if ' ' in value:
            raise ValueError("La contraseña no debe contener espacios.")
        if not any(char.isupper() for char in value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        return value

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: str = None
    email: EmailStr = None
    password: constr(min_length=8, max_length=16) = None # type: ignore # Restricción de longitud para contraseñas

    @validator('password')
    def no_spaces_in_password(cls, value):
        if value and ' ' in value:
            raise ValueError("La contraseña no debe contener espacios.")
        if not any(char.isupper() for char in value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        return value

@router.get("/{user_id}")
@limiter.limit("5/minute")  # Limitar a 5 peticiones por minuto
def find_user_by_id(
    user_id: int, 
    request: Request, db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    
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

@router.post("/login")
def login(
    user: UserLogin, 
    db: Session = Depends(get_db)
    ):
    
    repo = MySqlUserRepository(db)
    user_model = repo.find_by_username(user.username)

    if not user_model or user_model.password != user.password:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    access_token = create_access_token(data={"sub": user_model.username})
    return {"access_token": access_token, "token_type": "bearer"}

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
def update_user_by_id(
    user_id: int, 
    request:Request, user: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    
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
def delete_user_by_id(
    user_id: int, 
    request:Request, db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    
    repo = MySqlUserRepository(db)
    try:
        repo.delete_by_id(user_id)
        return {"message": f"User with ID {user_id} eliminated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

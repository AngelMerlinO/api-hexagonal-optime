from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.users.infrastructure.UserDependencies import get_user_service
from src.auth.jwt_handler import create_access_token, get_current_user
from config.database import get_db
from pydantic import BaseModel, EmailStr, constr, validator
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import Optional
import bcrypt

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/api/v1/users",
    tags=['users']
)

class UserCreate(BaseModel):
    contact_id: int
    username: str
    password: constr(min_length=8, max_length=16) # type: ignore

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
    username: Optional[str] = None
    password: Optional[constr(min_length=8, max_length=16)] = None # type: ignore

    @validator('password')
    def no_spaces_in_password(cls, value):
        if value and ' ' in value:
            raise ValueError("La contraseña no debe contener espacios.")
        if not any(char.isupper() for char in value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        return value

@router.post("/")
@limiter.limit("5/minute")
def create_user(
    request: Request,
    user: UserCreate,
    user_service=Depends(get_user_service)
):
    try:
        created_user = user_service.create_user(user.contact_id, user.username, user.password)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(
    request: Request,
    user: UserLogin,
    db: Session = Depends(get_db)
):
    user_service = get_user_service(db)
    user_model = user_service.user_by_username(user.username)

    if not user_model:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    
    # Verificar si la contraseña ingresada corresponde con el hash almacenado
    if not bcrypt.checkpw(user.password.encode('utf-8'), user_model.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    # Crear un token con el username
    access_token = create_access_token(data={"sub": user_model.username})
    
    # Retornar token y user_id
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_model.id  
    }

@router.get("/{user_id}")
@limiter.limit("5/minute")
def find_user_by_id(
    request: Request,
    user_id: int,
    user_service=Depends(get_user_service),
    current_user: str = Depends(get_current_user)
):
    try:
        user_with_contact = user_service.user_by_id(user_id)
        if not user_with_contact:
            raise HTTPException(status_code=404, detail="User not found")
        return user_with_contact
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error finding user by ID")

@router.put("/{user_id}")
@limiter.limit("2/minute")
def update_user_by_id(
    request: Request,  # Mueve `request` al primer lugar
    user_id: int,
    user: UserUpdate,
    user_service=Depends(get_user_service),
    current_user: str = Depends(get_current_user)
):
    try:
        user_service.update_user(
            identifier=user_id,
            username=user.username,
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
    request: Request,  # Mueve `request` al primer lugar
    user_id: int,
    user_service=Depends(get_user_service),
    current_user: str = Depends(get_current_user)
):
    try:
        user_service.delete_user(user_id)
        return {"message": f"User with ID {user_id} eliminated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
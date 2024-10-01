from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.users.application.UserCreator import UserCreator
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from config.database import get_db

app = FastAPI()

# Modelo Pydantic para la creación de un usuario
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    repo = MySqlUserRepository(db)
    user_creator = UserCreator(repo)
    try:
        user_creator.create(user.username, user.email, user.password)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
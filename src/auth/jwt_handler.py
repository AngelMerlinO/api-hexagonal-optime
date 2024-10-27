import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def create_access_token(data: dict):
    """
    Crea un token JWT con los datos del usuario y una fecha de expiración.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str):
    """
    Verifica el token JWT y devuelve los datos si es válido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extrae el token JWT de la solicitud y verifica su validez.
    """
    payload = verify_jwt_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return username

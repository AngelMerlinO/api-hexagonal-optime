import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv("config/.env", encoding="utf-8")

# Definir la base
Base = declarative_base()

# Intentar cargar DATABASE_URL directamente
DATABASE_URL = os.getenv('DATABASE_URL')

# Si DATABASE_URL no está configurado, construirla manualmente
if not DATABASE_URL:
    DB_USERSB = os.getenv('DB_USERSB')
    DB_PASSWORDSB = os.getenv('DB_PASSWORDSB')
    DB_HOSTSB = os.getenv('DB_HOSTSB')
    DB_PORTSB = os.getenv('DB_PORTSB')
    DB_NAMESB = os.getenv('DB_NAMESB')

    # Construir DATABASE_URL
    DATABASE_URL = f"mysql+pymysql://{DB_USERSB}:{DB_PASSWORDSB}@{DB_HOSTSB}:{DB_PORTSB}/{DB_NAMESB}"

# Crear el engine y la sesión
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

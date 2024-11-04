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
    DB_USERPG = os.getenv('DB_USERPG')
    DB_PASSWORDPG = os.getenv('DB_PASSWORDPG')
    DB_HOSTPG = os.getenv('DB_HOSTPG')
    DB_PORTPG = os.getenv('DB_PORTPG')
    DB_NAMEPG = os.getenv('DB_NAMEPG')

    # Construir DATABASE_URL
    DATABASE_URL = f"postgresql://{DB_USERPG}:{DB_PASSWORDPG}@{DB_HOSTPG}:{DB_PORTPG}/{DB_NAMEPG}"

# Crear el engine y la sesión
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

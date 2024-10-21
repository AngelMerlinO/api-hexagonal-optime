from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usar SQLite en memoria para pruebas
DATABASE_URL = "sqlite:///:memory:"

# Crear el motor y sesión de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir Base
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

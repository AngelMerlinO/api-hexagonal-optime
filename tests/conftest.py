import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base
from config.database import SessionLocal, engine as default_engine

@pytest.fixture(scope='function')
def db_session(monkeypatch):
    # Crear el engine para usar SQLite en memoria para las pruebas
    test_engine = create_engine("sqlite:///:memory:")

    # Crear todas las tablas en la base de datos en memoria
    Base.metadata.create_all(test_engine)

    # Mockear la conexión del motor de SQLAlchemy a SQLite
    session = sessionmaker(bind=test_engine)()

    # Parchar la sesión local para usar la sesión SQLite en lugar de MySQL
    monkeypatch.setattr('config.database.SessionLocal', lambda: session)

    yield session

    # Limpiar la base de datos después de cada prueba
    session.close()
    Base.metadata.drop_all(test_engine)

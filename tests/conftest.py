import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base, engine as default_engine  # Importar Base y el engine

@pytest.fixture(scope='function')
def db_session(monkeypatch):
    # Crear el engine para usar SQLite en memoria para las pruebas
    test_engine = create_engine("sqlite:///:memory:")

    # Crear todas las tablas en la base de datos en memoria
    Base.metadata.create_all(test_engine)

    # Mockear la sesión para que utilice SQLite
    session = sessionmaker(bind=test_engine)()

    # Parchar el engine y SessionLocal para usar SQLite en lugar de MySQL
    monkeypatch.setattr('config.database.engine', test_engine)
    monkeypatch.setattr('config.database.SessionLocal', lambda: session)

    yield session

    # Limpiar la base de datos después de cada prueba
    session.close()
    Base.metadata.drop_all(test_engine)

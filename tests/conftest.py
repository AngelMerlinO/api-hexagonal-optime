import pytest
from config.test_database import Base, engine, SessionLocal

@pytest.fixture(scope='function')
def db_session():
    # Crear todas las tablas en la base de datos en memoria para las pruebas
    Base.metadata.create_all(engine)

    session = SessionLocal()
    yield session

    # Limpiar la base de datos después de cada prueba
    session.close()
    Base.metadata.drop_all(engine)

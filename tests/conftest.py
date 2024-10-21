import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base
import os

@pytest.fixture(scope='session', autouse=True)
def use_sqlite_for_tests(monkeypatch):
    # Sobrescribir las variables de entorno para usar SQLite en memoria
    monkeypatch.setenv('DB_USER', '')
    monkeypatch.setenv('DB_PASSWORD', '')
    monkeypatch.setenv('DB_HOST', '')
    monkeypatch.setenv('DB_NAME', ':memory:')
    monkeypatch.setenv('DB_PORT', '')

    # Cambiar DATABASE_URL para que apunte a SQLite
    monkeypatch.setenv('DATABASE_URL', 'sqlite:///:memory:')

@pytest.fixture(scope='function')
def db_session():
    # Crear el engine para usar SQLite en memoria para las pruebas
    test_engine = create_engine("sqlite:///:memory:")

    # Crear todas las tablas en la base de datos en memoria
    Base.metadata.create_all(test_engine)

    # Crear sesión
    session = sessionmaker(bind=test_engine)()

    yield session

    # Limpiar la base de datos después de cada prueba
    session.close()
    Base.metadata.drop_all(test_engine)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base

@pytest.fixture(scope='function')
def db_session():
    # Configuración de la base de datos en memoria para pruebas
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)

    # Crea todas las tablas en la base de datos en memoria
    Base.metadata.create_all(engine)

    session = Session()
    yield session

    # Limpia la base de datos después de cada prueba
    session.close()
    Base.metadata.drop_all(engine)
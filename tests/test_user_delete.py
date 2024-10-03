import pytest
from fastapi.testclient import TestClient
from main import app 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base, get_db
from src.users.domain.User import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_delete_user(setup_database):
    response = client.post("/api/users/v1/", json={"username": "testuser", "email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    
    db = TestingSessionLocal()
    user = db.query(User).filter_by(email="test@example.com").first()
    assert user is not None   
    user_id = user.id

    response = client.delete(f"/api/users/v1/?user_id={user_id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"User with ID {user_id} eliminated successfully"}

    deleted_user = db.query(User).filter_by(id=user_id).first()
    assert deleted_user is None
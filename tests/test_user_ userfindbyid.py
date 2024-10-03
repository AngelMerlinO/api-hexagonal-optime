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

def test_find_user_by_id_success(setup_database):
    response = client.post("/api/users/v1/", json={"username": "testuser", "email": "test@example.com", "password": "password123"})
    assert response.status_code == 200

    db = TestingSessionLocal()
    user = db.query(User).filter_by(email="test@example.com").first()
    assert user is not None 
    user_id = user.id

    response = client.get(f"/api/users/v1/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"
    
def test_find_user_by_id_not_found(setup_database):
    non_existent_user_id = 9999
    response = client.get(f"/api/users/v1/{non_existent_user_id}")
    
    if response.status_code == 400:
        print(f"Error Message: {response.json()['detail']}")
    
    assert response.status_code in [400, 404], f"Unexpected status code {response.status_code}"
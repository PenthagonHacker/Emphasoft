import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from . import database
from .main import app

client = TestClient(app)


def test_get_user_by_id():
    """Test get user by id"""
    for id in (1, 2, 3, 4):
        if id in (1, 2, 3):
            response = client.get(f"/api/v1/users/{id}")
            assert response.status_code == 200
        if id == 4:
            response = client.get(f"/api/v1/users/{id}")
            assert response.status_code == 400


@pytest.fixture
def get_db():
    return database.SessionLocal()


@pytest.fixture
def user_data(get_db: Session):
    data = {
        "username": "John",
        "first_name": "Doe",
        "last_name": "Test",
        "password": "TestPassword",
        "is_active": True,
    }
    yield data
    get_db.query(database.User).filter(
        database.User.username == data["username"]
    ).delete()
    get_db.commit()


def test_create_new_user(user_data):
    """Test create new user"""
    response = client.post(
        "/api/v1/users/",
        headers={"WWW-Authenticate": "Bearer"},
        json=user_data,
    )
    assert response.status_code == 201

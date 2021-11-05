import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .database import SessionLocal, User
from .main import app

client = TestClient(app)


def test_get_user_by_id():
    for id in (1, 2, 3, 4):
        if id in (1, 2, 3):
            response = client.get(f'/api/v1/users/{id}')
            assert response.status_code == 200
        if id == 4:
            response = client.get(f'/api/v1/users/{id}')
            assert response.status_code == 400


@pytest.fixture
def get_db():
    return SessionLocal()


@pytest.fixture
def user_data(get_db: Session):
    data = {
        'username': 'Test',
        'first_name': 'Test',
        'last_name': 'Test',
        'password': 'TestPassword',
        'is_active': True
    }
    yield data
    print(get_db.query(User).filter(User.username == 'Test'))
    # get_db.query(User).filter(User.username == 'Test').delete()


def test_create_new_user(user_data):
    response = client.post(
        '/api/v1/users/',
        headers={"WWW-Authenticate": "Bearer"},
        json={
            'username': 'Test',
            'first_name': 'Test',
            'last_name': 'Test',
            'password': 'TestPassword',
            'is_active': True
        },
    )
    assert response.status_code == 201

import pytest
from faker import Faker
from Models import UserRequest
import requests

fake = Faker()


@pytest.fixture(scope="session")
def create_user():
    data = {
        "name": fake.name(),
        "job": fake.job(),
    }
    user = UserRequest(**data)
    response = requests.post('https://reqres.in/api/users', json=user.model_dump())
    assert response.status_code == 201, f"Failed to create user: {response.json()}"

    user_id = response.json()['id']
    yield user_id, user
    delete_response = requests.delete(f'https://reqres.in/api/users/{user_id}')
    assert delete_response.status_code == 204, f"Failed to delete user: {delete_response.json()}"
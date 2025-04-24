import requests
from Models import ResponseModel
from Models import UserResponse
from faker import Faker
from Models import UpdateUserRequest
from Models import UpdateUserResponse
from datetime import datetime
from conftest import create_user
fake = Faker()


def test_users_pagination():
    response = requests.get('https://reqres.in/api/users?page=1')
    assert response.status_code == 200

    response_data = ResponseModel(**response.json())

    assert len(response_data.data) == response_data.per_page, 'Количество пользователей не совпадает с per_page'
    assert response_data.page > 0, 'Текущая страница должна быть больше 0'
    assert response_data.per_page > 0, 'Количество элементов на странице должно быть больше 0'
    assert response_data.total >= len(
        response_data.data), 'Общее количество элементов должно быть больше или равно количеству полученных данных'
    assert response_data.total_pages > 0, 'Общее количество страниц должно быть больше 0'

    print('Все проверки пройдены успешно!')

def test_user(create_user):
    user_id = create_user
    response = requests.get(f'https://reqres.in/api/users/{user_id}')
    assert response.status_code == 200, f"User not found: {response.json()}"
    user_data = UserResponse(**response.json())
    assert user_data.data.id == user_id
    print(user_data)


def test_create_user(create_user):
    user_id, user = create_user
    response = requests.get(f'https://reqres.in/api/users/{user_id}')
    assert response.status_code == 200

    response_data = UserResponse(**response.json())
    assert response_data.id == user_id
    assert response_data.name == user.name
    assert response_data.job == user.job
    assert response_data.createdAt is not None


def test_update_user(create_user):
    user_id = create_user
    new_user_update = UpdateUserRequest(
        name=fake.name(),
        job=fake.job()
    )
    response = requests.patch(url=f'https://reqres.in/api/users/{user_id}', json=new_user_update.model_dump())
    assert response.status_code == 200
    response_data = UpdateUserResponse(**response.json())
    assert response_data.name == new_user_update.name
    assert response_data.job == new_user_update.job
    assert response_data.updatedAt is not None
    assert isinstance(response_data.updatedAt, datetime)
    print(f'Пользователь успешно обновлен{response.json()}')

def test_delete_user(create_user):
    user_id = create_user
    response = requests.delete(f'https://reqres.in/api/users/{user_id}')
    assert response.status_code == 204

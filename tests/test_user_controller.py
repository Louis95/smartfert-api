from tests.fixtures import *


def test_create_user_success(client):
    """Test case: Valid user data provided"""

    data = {
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'password123',
        'username': 'newtestuser@example.com'
    }
    delete_user_from_db('newtestuser@example.com')
    response = client.post('/register', json=data)
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'


def test_create_user_existing(client):
    """Test case: User with the same username already exists"""
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'password123',
        'username': 'johndoe@example.com'
    }

    client.post('/register', json=data)

    response = client.post('/register', json=data)
    assert response.status_code == 400
    assert response.json['message'] == 'User already exists. Please log in.'


def test_create_user_missing_data(client):
    """Test case: Required data is missing"""
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
    }

    response = client.post('/register', json=data)
    assert response.status_code == 400
    assert 'Input payload validation failed' in response.json['message']


def test_user_login_success(client):
    user_data = {
        "username": "testuser@example.com",
        "password": "password123"
    }
    response = client.post('/login/', json=user_data)
    assert response.status_code == 200
    assert response.json['message'] == 'Successfully logged in.'


def test_user_login_invalid_credentials(client):
    user_data = {
        "username": "testuser@example.com",
        "password": "password1"
    }
    response = client.post('/login/', json=user_data)
    print(response.json)
    assert response.status_code == 401
    assert response.json['message'] == 'Username or password does not match.'




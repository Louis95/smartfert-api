import pytest

from tests.fixtures import *


def test_get_farm_success(client: FlaskClient, access_token: str, create_test_farm) -> None:
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/farm/', headers=headers)
    assert response.status_code == 200
    data = response.json
    assert 'data' in data
    assert len(data['data']) > 0


def test_get_farm_unauthorized(client):
    response = client.get('/farm/', headers={'Authorization': ''})
    assert response.status_code == 401


def test_get_farm_not_found(client, access_token_user_with_no_data):
    response = client.get('/farm/', headers={'Authorization': f'Bearer {access_token_user_with_no_data}'})
    assert response.status_code == 404

from tests.fixtures import *


def test_get_fertilizer_with_default_date_success(client: FlaskClient, access_token: str) -> None:
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/fertilizer/b63b34ee-242e-454e-9a10-6870abb08c90/', headers=headers)
    assert response.status_code == 404


def test_get_fertilizer_unauthorized(client):
    response = client.get('/fertilizer/b63b34ee-242e-454e-9a10-6870abb08c90?date=2022-02-02', headers={'Authorization': ''})
    assert response.status_code == 401


def test_fertilizer_success(client, access_token, create_test_fertilizer, create_test_farm):
    print(f"access_token:{access_token}")
    response = client.get(f'/fertilizer/{create_test_farm.id}?date=2022-02-02', headers={'Authorization': f'Bearer {access_token}'})

    data = response.json
    assert response.status_code == 200
    assert 'data' in data
    assert 'locations' in data['data']
    assert 'total' in data['data']
    assert len(data['data']) > 0


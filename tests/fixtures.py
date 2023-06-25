import pytest
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from main import db
from main.models.farm_model.farm_model import FarmModel
from main.models.fertilizer_model.fertilizer_model import FertilizerModel
from main.models.user_model.user import User
from manage import app


@pytest.fixture
def client() -> FlaskClient:
    with app.test_client() as client:
        yield client


@pytest.fixture
def create_test_user():
    test_user = User(username='user@example.com',
                     first_name='first', last_name='last', password='123456789')
    existing_user = User.query.filter_by(username='user@example.com').first()
    if existing_user:
        return existing_user
    else:
        db.session.add(test_user)
        db.session.commit()
        return test_user


@pytest.fixture
def create_test_farm(create_test_user):
    test_farm = FarmModel(name="Test farm", user_id=1)
    existing_farm = FarmModel.query.filter_by(name='Test farm').first()

    if existing_farm:
        return existing_farm
    else:
        db.session.add(test_farm)
        db.session.commit()
        return test_farm


@pytest.fixture
def access_token() -> str:
    with app.app_context():
        token = create_access_token(identity=1)
        yield token


@pytest.fixture
def access_token_user_with_no_data() -> str:
    with app.app_context():
        token = create_access_token(identity=900)
        yield token


@pytest.fixture
def create_test_fertilizer(create_test_farm):
    test_fertilizer = FertilizerModel(location=f'POINT({59.91291350220959} {10.668913280301501})', date='2022-02-02', nit=2.84,
                                      farm_id=create_test_farm.id)
    db.session.add(test_fertilizer)
    db.session.commit()
    return test_fertilizer


def delete_user_from_db(username: str):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
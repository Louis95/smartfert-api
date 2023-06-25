
from typing import Dict, Tuple

from main.utilities.utilities import save_changes
from main.models.user_model.user import User
from flask_jwt_extended import create_access_token


def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """
    Logs in a user.

    Args:
        data (Dict[str, str]): User data including email and password.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing response object and HTTP status code.
    """
    try:
        user = User.query.filter_by(username=data.get('username')).first()
        if not user:
            return {'message': 'Username or password does not match.'}, 401

        if not user or not user.check_password(data.get('password')):
            return {'message': 'Username or password does not match.'}, 401

        access_token = create_access_token(identity=user.id)
        if access_token:
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'access_token': access_token
            }
            return response_object, 200

    except Exception as e:
        return {"message": f"An error occurred, please try again. Error: {e}"}, 500


def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """
    Saves a new user.

    Args:
        data (Dict[str, str]): User data including username, password, first name, and last name.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing response object and HTTP status code.
    """
    try:
        user = User.query.filter_by(username=data['username']).first()

        if user:
            return {'message': 'User already exists. Please log in.'}, 400

        new_user = User(
            username=data.get('username'),
            password=data.get('password'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        save_changes(new_user)

        return {'message': "User registered successfully", 'access_token': create_access_token(identity=new_user.id)}, 201
    except Exception as e:
        return {"message": f"An error occurred, please try again. Error: {e}"}, 500

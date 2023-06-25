from flask import request
from flask_restx import Api, Resource

from main.utilities.dto import UserDto
from main.services.user_service import save_new_user, login_user

user_ns = UserDto.user_ns
_user = UserDto.user
_auth_user = UserDto.user_auth


class Users(Resource):
    @user_ns.expect(_user, validate=True)
    @user_ns.response(201, 'User successfully created.')
    @user_ns.response(400, "User already exist")
    @user_ns.doc('New user registration')
    def post(self):
        """
        Register a new user.

        This endpoint allows users to register a new account by providing the required information.

        Payload:
        - first_name (string): First name of the user.
        - last_name (string): Last name of the user.
        - email (string): Email address of the user.
        - password (string): Password for the user's account.
        - username (string): Username for the user's account.

        Returns:
        - 201: User successfully created with token.
        """
        return save_new_user(data=request.json)


class UserLogin(Resource):
    @user_ns.doc('User login')
    @user_ns.response(401, 'Unauthorized')
    @user_ns.response(200, 'Login successful')
    @user_ns.expect(_auth_user, validate=True)
    def post(self):
        """
        Login a user.

        This endpoint allows users to log in by providing their login credentials.

        Payload:
        - email (string): Email address of the user.
        - password (string): Password for the user's account.

        Returns:
        - 200: Login successful.
        - 401: Unauthorized access, either the provided credentials are incorrect or the user is not authorized.
        - 400: Missing or invalid JSON in the request.
        """
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400

        user_data = request.json
        return login_user(user_data)

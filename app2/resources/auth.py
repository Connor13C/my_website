from hmac import compare_digest
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from input_handling import sanitize_input
from models.auth import JwtBlocklist
from models.parser import Parser
from models.user import UserModel


class UserRegister(Resource):
    """User registration endpoint for url /register not secure for demo only"""
    parser = Parser()
    parser.required_fields('username', 'password')
    @classmethod
    def post(cls):
        """Post endpoint for registering users into the database.
        Takes params username and password to put into database. Usernames
        cannot be duplicated and will return json message and 400 error if tried.
        On successful user creation will return json message and 201 code"""
        req = cls.parser.parse_args()
        data = {
            'username': sanitize_input(req['username']),
            'password': sanitize_input(req['password'])
        }
        if UserModel.find_by_username(data['username']):
            return {'message': f'User with name {data["username"]} already exists'}, 400
        UserModel(**data).save_to_db()
        return data, 201


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted'}
        return {'message': 'User not found'}, 404


class UserLogin(Resource):
    parser = Parser()
    parser.required_fields('username', 'password')
    @classmethod
    def post(cls):
        req = cls.parser.parse_args()
        username = sanitize_input(req['username'])
        password = sanitize_input(req['username'])
        user = UserModel.find_by_username(username)
        if user and safe_str_cmp(user.password, password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(str(user.id))
            return {'access_token': access_token, 'refresh_token': refresh_token}
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_jwt()['jti']
        JwtBlocklist(id=jti).save_to_db()
        return {'message': 'User successfully logged out.'}


"""
This module mocks an interaction with an OAuth2 Authorization Server.
"""


def introspect_token(access_token):
    """
    Uses hard-coded tokens to map to hard-coded user information
    """
    token_mapping = {
        "31cd894de101a0e31ec4aa46503e59c8": {
            "token_is_valid": True,
            "user_info": {
                "user_id": "8bde3e84-a964-479c-9c7b-4d7991717a1b",
                "username": "challengeuser1",
            },
        },
        "97778661dab9584190ecec11bf77593e": {
            "token_is_valid": True,
            "user_info": {
                "user_id": "45e3c49a-c699-405b-a8b2-f5407bb1a133",
                "username": "challengeuser2",
            },
        },
    }

    invalid_response = {"token_is_valid": False, "user_info": None}

    return token_mapping.get(access_token, invalid_response)


def safe_str_cmp(a: str, b: str) -> bool:
    """This function compares strings in somewhat constant time. This
    requires that the length of at least one string is known in advance.

    Returns `True` if the two strings are equal, or `False` if they are not.
    """

    if isinstance(a, str):
        a = a.encode("utf-8")  # type: ignore

    if isinstance(b, str):
        b = b.encode("utf-8")  # type: ignore

    return compare_digest(a, b)

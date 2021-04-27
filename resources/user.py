import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help="This field is required")
_user_parser.add_argument('password', type=str, required=True, help="This field is required")


class UserRegister(Resource):
    @staticmethod
    def post():
        data: dict = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': f"A user with name {data['username']} already exists."}, 400

        user = UserModel(**data)
        user.save()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    @jwt_required()
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        return user.json()

    @classmethod
    @jwt_required()
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        user.delete()
        return {'message': 'User deleted.'}


class UserLogin(Resource):
    @staticmethod
    def post():
        data: dict = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200

        return {'message': 'Invalid credentials.'}, 401


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}

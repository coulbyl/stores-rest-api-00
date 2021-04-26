import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field is required")
    parser.add_argument('password', type=str, required=True, help="This field is required")

    @classmethod
    def post(cls):
        data: dict = cls.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': f"A user with name {data['username']} already exists."}, 400

        user = UserModel(**data)
        user.save()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        user.delete()
        return {'message': 'User deleted.'}

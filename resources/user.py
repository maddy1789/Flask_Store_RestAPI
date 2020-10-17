from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.user import UserModel

_user_parser = reqparse.RequestParser()

_user_parser.add_argument("username",
    type=str,
    required=True,
    help="Username is required"
)

_user_parser.add_argument("password", 
    type=str,
    required=True,
    help="Password is required"
)


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "Username already exists!"}, 400

        user = UserModel(**data)
        try:
            user.save_to_db()
        except:
            return {"message": "Something went wrong"}, 500

        return {"message": "User Created!", "user": user.json()}, 201


class User(Resource):
    
    @jwt_required()
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {"message": "User not found!"}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete()
            return {"message": "User Deleted!"}
        return {"message": "User not found!"}, 404 
        
    
class UserList(Resource):

    @jwt_required()
    def get(self):
        return {"users": [user.json() for user in UserModel.find_all()]}
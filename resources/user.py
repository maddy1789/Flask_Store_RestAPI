
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
                                jwt_required,
                                fresh_jwt_required, 
                                get_jwt_claims,
                                jwt_optional, 
                                get_jwt_identity
                            )

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

    @fresh_jwt_required
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
    
    @jwt_required
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {"message": "User not found!"}, 404

    @jwt_required
    def delete(self, user_id):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Admin privileges required!"}, 401
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete()
            return {"message": "User Deleted!"}
        return {"message": "User not found!"}, 404 
        
    
class UserList(Resource):

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        users = [user.json() for user in UserModel.find_all()]
        if user_id:
            return {"users": users}
        return {"users": [user["username"] for user in users],
                "message": "For more details kindly login"        
        }



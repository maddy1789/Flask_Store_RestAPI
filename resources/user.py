from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.user import UserModel

class User(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("password", 
        type=str,
        required=True,
        help="Password is required"
    )

    @jwt_required()
    def get(self, uname):
        user = UserModel.find_by_username(uname)
        if user:
            return user.json()
        return {"message": "Username not found!"}, 404
        
    @jwt_required()
    def post(self, uname):
        data = User.parser.parse_args()

        if UserModel.find_by_username(uname):
            return {"message": "Username already exists!"}

        user = UserModel(uname, data["password"])
        try:
            user.save_to_db()
        except:
            return {"message": "Something went wrong"}, 500

        return {"message": "User Created!", "user": user.json()}, 201


class UserList(Resource):
    @jwt_required()
    def get(self):
        return {"users": [user.json() for user in UserModel.query.all()]}
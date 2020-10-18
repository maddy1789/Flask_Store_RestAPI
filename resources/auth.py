from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token,
                                get_jwt_identity,
                                jwt_refresh_token_required,
                                jwt_required,
                                get_raw_jwt
                                )
from blacklist import BLACKLIST

from models.user import UserModel

class UserLogin(Resource):
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

    def post(self):
        data = self._user_parser.parse_args()

        user = UserModel.find_by_username(data["username"])
        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid Credentials!"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"] # jti is JWT ID, a unique identifier
        BLACKLIST.add(jti)
        return {"message": "Successfully Logged Out."}
        

class TokenRefresh(Resource):
    
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": access_token}, 200

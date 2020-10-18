from flask import Flask, jsonify
from flask_restful import Api
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager

from security import authenticate, identity
from blacklist import BLACKLIST
from resources.user import User, UserList, UserRegister
from resources.auth import UserLogin, TokenRefresh, UserLogout
from resources.store import Store, StoreList
from resources.item import Item, ItemList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.secret_key = "q1w2e3r4t5y6"
api = Api(app)

jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token():
    return jsonify({
        "description": "The token has expired!",
        "error": "Token Expired"
    }), 401

@jwt.invalid_token_loader
def invalid_token(error):
    return jsonify({
        "description": "Signature verification failed!",
        "error": "Token Invalid"
    }), 401

@jwt.unauthorized_loader
def unauthorized(error):
    return jsonify({
        "description": "Request contain Unauthorized Access",
        "error": "Authentication Required"
    }), 401

@jwt.needs_fresh_token_loader
def fresh_token():
    return jsonify({
        "description": "The token is not fresh",
        "error": "Fresh Token Required"
    }), 401

@jwt.revoked_token_loader
def revoked_token():
    return jsonify({
        "description": "The token has been revoked",
        "error": "Revoked Token"
    }), 401

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}

@jwt.token_in_blacklist_loader
def blacklist_token(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(User, "/user/<string:user_id>")
api.add_resource(UserList, "/users")
api.add_resource(UserRegister, "/register")

api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

api.add_resource(Store, "/store/<string:sname>")
api.add_resource(StoreList, "/stores")

api.add_resource(Item, "/item/<string:iname>")
api.add_resource(ItemList, "/items")
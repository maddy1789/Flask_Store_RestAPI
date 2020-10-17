from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import User, UserList, UserRegister
from resources.store import Store, StoreList
from resources.item import Item, ItemList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "q1w2e3r4t5y6"
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(User, "/user/<string:user_id>")
api.add_resource(UserList, "/users")
api.add_resource(UserRegister, "/register")

api.add_resource(Store, "/store/<string:sname>")
api.add_resource(StoreList, "/stores")

api.add_resource(Item, "/item/<string:iname>")
api.add_resource(ItemList, "/items")











 
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel

class Store(Resource):

    @jwt_required()
    def get(self, sname):
        store = StoreModel.find_by_name(sname)
        if store:
            return store.json()
        return {"message": "Store Not Found!"}, 404

    @jwt_required()
    def post(self, sname):
        if StoreModel.find_by_name(sname):
            return {"message": "Store already exist!"}, 400

        store = StoreModel(sname)
        store.save_to_db()
        return {"message": "Store created!", "store": store.json()}, 201

    @jwt_required()
    def delete(self, sname):
        store = StoreModel.find_by_name(sname)
        if store:
            store.delete()
            return {"message": "Store Deleted!"}
        return {"message": "Store Not Found!"}, 404


class StoreList(Resource):

    @jwt_required()
    def get(self):
        return {"stores": [store.json() for store in StoreModel.find_all()]}
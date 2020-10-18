from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, 
                                fresh_jwt_required,
                                get_jwt_claims, 
                                jwt_optional, 
                                get_jwt_identity
                            )
from models.store import StoreModel

class Store(Resource):

    @jwt_required
    def get(self, sname):
        store = StoreModel.find_by_name(sname)
        if store:
            return store.json()
        return {"message": "Store Not Found!"}, 404

    @fresh_jwt_required
    def post(self, sname):
        if StoreModel.find_by_name(sname):
            return {"message": "Store already exist!"}, 400

        store = StoreModel(sname)
        store.save_to_db()
        return {"message": "Store created!", "store": store.json()}, 201

    @jwt_required
    def delete(self, sname):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Admin privileges required!"}, 401
        store = StoreModel.find_by_name(sname)
        if store:
            store.delete()
            return {"message": "Store Deleted!"}
        return {"message": "Store Not Found!"}, 404


class StoreList(Resource):

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        stores = [store.json() for store in StoreModel.find_all()]
        if user_id:
            return {"stores": stores}
        return {"stores": [store["store"] for store in stores],
            "message": "For more details kindly login"        
        } 
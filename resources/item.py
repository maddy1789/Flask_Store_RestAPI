from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("price",
        type=float,
        required=True,
        help="Item Price is required"
    )

    parser.add_argument("store_id",
        type=int,
        required=True,
        help="Store ID is required"
    )

    @jwt_required()
    def get(self, iname):
        item = ItemModel.find_by_name(iname)
        if item:
            return item.json()
        return {"message": "Item Not Found!"}, 404

    @jwt_required()
    def post(self, iname):
        if ItemModel.find_by_name(iname):
            return {"message": "Item already exist!"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(iname, **data)

        item.save_to_db()

        return {"message": "Item created!", "item": item.json()}, 201

    @jwt_required()
    def put(self, iname):
        item = ItemModel.find_by_name(iname)
        data = Item.parser.parse_args()

        if item:
            item.price = data["price"]
        else:
            item = ItemModel(iname, **data)
        item.save_to_db()

        return {"message": "Item Updated!", "item": item.json()} 
        
    @jwt_required()
    def delete(self, iname):
        item = ItemModel.find_by_name(iname)
        if item:
            item.delete()
            return {"message": "Item Deleted!"}
        return {"message": "Item Not Found!"}, 404


class ItemList(Resource):

    @jwt_required()
    def get(self):
        return {"items": [item.json() for item in ItemModel.find_all()]}
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank.")
    parser.add_argument('store_id', type=int, required=True, help="Every item neends a store id.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name {name} already exists."}, 400  # bad request

        data: dict = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save()
        except (ValueError, Exception):
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201  # created

    @jwt_required()
    def delete(self, name):
        claims = get_jwt_identity()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        item = ItemModel.find_by_name(name)

        if item is None:
            return {'message': f"An item with name {name} not exists."}, 400

        item.delete()
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data: dict = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
            item.save()
        else:
            item.price = data['price']
            item.save()

        return item.json()


class ItemList(Resource):
    @staticmethod
    @jwt_required(optional=True)
    def get():
        return {"items": [item.json() for item in ItemModel.find_all()]}

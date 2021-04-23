from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        return {"message": "Store not found."}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"A store with name <-- {name} --> already exists."}

        store = StoreModel(name)
        try:
            store.save()
        except:
            return {"message": "An error occurred while creating a store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        print('from store ------- ', store.json())
        if store:
            store.delete()
            return {"message": "Store deleted!"}

        return {"message": "Store not found."}, 404


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}

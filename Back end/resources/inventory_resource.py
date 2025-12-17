from flask_restful import Resource
from Models import Inventory

class InventoryListResource(Resource):
    def get(self):
        return [
            {"id": i.id, "product_name": i.product_name, "stock": i.stock}
            for i in Inventory.query.all()
        ]

from flask import request
from flask_restful import Resource
from services.inventory_service import InventoryService

class InventoryCheckResource(Resource):
    def get(self, product_id):
        qty = InventoryService.check_stock(product_id)
        if qty is None:
            return {'message': 'Product not found'}, 404
        
        # Requirement says "Check stock availability", implies returning stock count or boolean?
        # Hint says "return product_data".
        # Let's return details.
        product = InventoryService.get_product(product_id)
        return product.to_dict(), 200

class InventoryUpdateResource(Resource):
    def put(self):
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
            
        product_id = data.get('product_id')
        quantity_change = data.get('quantity_change') # requirement says "Update inventory"
        
        # We need to handle schema "update inventory after order".
        # If input is different, adjust.
        # Assuming {product_id: 1, quantity_change: 2} means reduce by 2?
        # My service logic assumes quantity_change > 0 reduces stock?
        # "new_quantity = product.quantity_available - quantity_change" in service.
        
        try:
             updated_product = InventoryService.update_stock(product_id, quantity_change)
             if updated_product:
                 return {'message': 'Stock updated', 'product': updated_product.to_dict()}, 200
             return {'message': 'Product not found'}, 404
        except ValueError as e:
            return {'message': str(e)}, 400

from models import Inventory
from extensions import db

class InventoryService:

    @staticmethod
    def get_product(product_id):
        return Inventory.query.get(product_id)

    @staticmethod
    def check_stock(product_id):
        product = Inventory.query.get(product_id)
        if product:
            return product.quantity_available
        return None

    @staticmethod
    def get_all_products():
        return Inventory.query.all()

    @staticmethod
    def update_stock(product_id, quantity_change):
        
        product = Inventory.query.get(product_id)
        if not product:
            return None
        
        new_quantity = product.quantity_available - quantity_change
        if new_quantity < 0:
             raise ValueError("Insufficient stock")
        
        product.quantity_available = new_quantity
        db.session.commit()
        return product

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
    def update_stock(product_id, quantity_change):
        # Quantity change can be negative (reduce stock) or positive (restock)
        # Note: Requirement says "Update inventory after order", likely reduce.
        # But method signature in requirements is nonspecific, so I'll assume explicit set or reduce.
        # "Update stock quantities after order placement" -> reduce.
        product = Inventory.query.get(product_id)
        if not product:
            return None
        
        new_quantity = product.quantity_available - quantity_change
        if new_quantity < 0:
             raise ValueError("Insufficient stock")
        
        product.quantity_available = new_quantity
        db.session.commit()
        return product

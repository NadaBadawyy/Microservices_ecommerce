from Models import Inventory
from extensions import db

class InventoryService:

    @staticmethod
    def reduce_stock(product_id, quantity):
        inventory = Inventory.query.get_or_404(product_id)
        if inventory.stock < quantity:
            raise ValueError("Not enough stock")
        inventory.stock -= quantity
        db.session.commit()

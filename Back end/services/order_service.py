from Models import Order
from extensions import db

class OrderService:

    @staticmethod
    def create_order(product_id, quantity, total_price):
        order = Order(
            product_id=product_id,
            quantity=quantity,
            total_price=total_price
        )
        db.session.add(order)
        db.session.commit()
        return order

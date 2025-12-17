import requests
from models import Order, OrderItem
from extensions import db

class OrderService:
    INVENTORY_SERVICE_URL = "http://localhost:5002/api/inventory"

    @staticmethod
    def create_order(customer_id, products, total_amount):
        # 1. Validate inputs (basic check)
        if not products:
            raise ValueError("No products in order")

        # 2. Check stock for all products
        # We can optimize this but doing sequential checks for now
        for item in products:
            p_id = item['product_id']
            qty = item['quantity']
            
            try:
                resp = requests.get(f"{OrderService.INVENTORY_SERVICE_URL}/check/{p_id}")
                if resp.status_code != 200:
                    raise ValueError(f"Product {p_id} not found")
                
                data = resp.json()
                if data['quantity_available'] < qty:
                    raise ValueError(f"Insufficient stock for product {p_id}")
            except requests.exceptions.RequestException:
                 raise ValueError("Inventory Service unavailable")

        # 3. Create Order
        new_order = Order(
            customer_id=customer_id,
            total_amount=total_amount,
            status='CONFIRMED' # Immediate confirmation as per flow? Or PENDING then CONFIRMED?
        )
        db.session.add(new_order)
        db.session.flush() # Get ID

        # 4. Save Order Items and Deduct Stock
        for item in products:
            p_id = item['product_id']
            qty = item['quantity']
            
            # Save Item (price is needed, maybe get from Inventory check? 
            # For now assuming total_amount covers it or simplified)
            # Todo: Need price per item. 
            # Let's assume we call Inventory Update which acts as "Commit"
            
            # Deduction
            requests.put(f"{OrderService.INVENTORY_SERVICE_URL}/update", json={
                'product_id': p_id,
                'quantity_change': qty # Positive value to reduce? Update method I wrote reduces if positive.
            })

            order_item = OrderItem(
                order_id=new_order.order_id,
                product_id=p_id,
                quantity=qty,
                unit_price=0 # Placeholder, ideally strictly calculated
            )
            db.session.add(order_item)

        db.session.commit()
        return new_order

    @staticmethod
    def get_order(order_id):
        return Order.query.get(order_id)

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.query.filter_by(customer_id=customer_id).all()

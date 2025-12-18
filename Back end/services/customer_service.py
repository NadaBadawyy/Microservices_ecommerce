import requests
from models import Customer, Order
from extensions import db

class CustomerService:
    ORDER_SERVICE_URL = "http://localhost:5001/api/orders"

    @staticmethod
    def get_customer(customer_id):
        return Customer.query.get(customer_id)

    @staticmethod
    def get_all_customers():
        return Customer.query.all()

    @staticmethod
    def get_customer_orders(customer_id):
        # Call Order Service to get orders for this customer
        # Requirement: GET /api/customers/{customer_id}/orders -> calls Order Service
        try:
            # Order Service needed endpoint: GET /api/orders?customer_id=X
            response = requests.get(f"{CustomerService.ORDER_SERVICE_URL}", params={'customer_id': customer_id})
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return []

    @staticmethod
    def update_loyalty_points(customer_id, points):
        customer = Customer.query.get(customer_id)
        if customer:
            customer.loyalty_points += points
            db.session.commit()
            return customer
        return None
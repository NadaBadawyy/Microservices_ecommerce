from flask import request
from flask_restful import Resource
from services.customer_service import CustomerService

class CustomerResource(Resource):
    def get(self, customer_id):
        customer = CustomerService.get_customer(customer_id)
        if customer:
            return customer.to_dict(), 200
        return {'message': 'Customer not found'}, 404

class CustomerOrdersResource(Resource):
    def get(self, customer_id):
        orders = CustomerService.get_customer_orders(customer_id)
        return orders, 200

class CustomerLoyaltyResource(Resource):
    def put(self, customer_id):
        # Input: {points: 10}
        data = request.get_json()
        points = data.get('points', 0)
        
        updated = CustomerService.update_loyalty_points(customer_id, points)
        if updated:
            return {'message': 'Loyalty updated', 'customer': updated.to_dict()}, 200
        return {'message': 'Customer not found'}, 404
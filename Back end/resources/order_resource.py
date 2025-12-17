from flask import request
from flask_restful import Resource
from services.order_service import OrderService

class OrderCreateResource(Resource):
    def post(self):
        data = request.get_json()
        # Input: {customer_id: 1, products: [...], total_amount: 100}
        
        try:
            customer_id = data.get('customer_id')
            products = data.get('products')
            total_amount = data.get('total_amount')
            
            order = OrderService.create_order(customer_id, products, total_amount)
            return {'message': 'Order created', 'order': order.to_dict()}, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f"Server Error: {str(e)}"}, 500

class OrderDetailResource(Resource):
    def get(self, order_id):
        order = OrderService.get_order(order_id)
        if order:
            return order.to_dict(), 200
        return {'message': 'Order not found'}, 404

class OrderListResource(Resource):
    # Support "GET /api/orders?customer_id=X"
    def get(self):
        customer_id = request.args.get('customer_id')
        if customer_id:
            orders = OrderService.get_orders_by_customer(customer_id)
            return [o.to_dict() for o in orders], 200
        return [], 200



from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)


orders_db = {}
order_counter = 1


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'service': 'Order Service',
        'status': 'healthy',
        'port': 5001,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/orders/create', methods=['POST'])
def create_order():
    """
    Create new order
    Expected JSON:
    {
        "customer_id": 1,
        "products": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 3, "quantity": 1}
        ],
        "total_amount": 1299.99
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'customer_id' not in data:
            return jsonify({'error': 'customer_id is required'}), 400
        
        if 'products' not in data or not isinstance(data['products'], list):
            return jsonify({'error': 'products list is required'}), 400
        
        if 'total_amount' not in data:
            return jsonify({'error': 'total_amount is required'}), 400
        
        if len(data['products']) == 0:
            return jsonify({'error': 'At least one product is required'}), 400
        
        for product in data['products']:
            if 'product_id' not in product or 'quantity' not in product:
                return jsonify({'error': 'Each product must have product_id and quantity'}), 400
            
            if product['quantity'] <= 0:
                return jsonify({'error': 'Quantity must be greater than 0'}), 400
        
        global order_counter
        order_id = order_counter
        order_counter += 1
        
        order = {
            'order_id': order_id,
            'customer_id': data['customer_id'],
            'products': data['products'],
            'total_amount': float(data['total_amount']),
            'status': 'CONFIRMED',
            'created_at': datetime.now().isoformat()
        }
        
        orders_db[order_id] = order
        
        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'order': order
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Retrieve order details by order ID"""
    try:
        if order_id not in orders_db:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({
            'success': True,
            'order': orders_db[order_id]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@app.route('/api/orders', methods=['GET'])
def get_orders_by_customer():
    """Get all orders for a customer"""
    try:
        customer_id = request.args.get('customer_id', type=int)
        
        if not customer_id:
            return jsonify({'error': 'customer_id parameter is required'}), 400
        
        customer_orders = [
            order for order in orders_db.values() 
            if order['customer_id'] == customer_id
        ]
        
        return jsonify({
            'success': True,
            'customer_id': customer_id,
            'order_count': len(customer_orders),
            'orders': customer_orders
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 ORDER SERVICE STARTING")
    print("=" * 50)
    print("Port: 5001")
    print("Endpoints:")
    print("  - GET  /health")
    print("  - POST /api/orders/create")
    print("  - GET  /api/orders/<order_id>")
    print("  - GET  /api/orders?customer_id=<id>")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
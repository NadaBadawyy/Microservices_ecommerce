

from flask import Flask, request, jsonify
import mysql.connector
import requests
from datetime import datetime

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'ecommerce_user',
    'password': 'ecommerce_pass123',
    'database': 'ecommerce_system'
}


CUSTOMER_SERVICE_URL = 'http://localhost:5003'
INVENTORY_SERVICE_URL = 'http://localhost:5004'
ORDER_SERVICE_URL = 'http://localhost:5001'


def get_db_connection():
    """Create and return database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    conn = get_db_connection()
    db_status = 'connected' if conn else 'disconnected'
    if conn:
        conn.close()
    
    return jsonify({
        'service': 'Notification Service',
        'status': 'healthy',
        'port': 5005,
        'database': db_status,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/notifications/send', methods=['POST'])
def send_notification():
    """
    Send order notification
    Expected JSON:
    {
        "order_id": 1,
        "customer_id": 1,
        "notification_type": "order_confirmation"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        order_id = data.get('order_id')
        customer_id = data.get('customer_id')
        notification_type = data.get('notification_type', 'order_confirmation')
        
        if not order_id or not customer_id:
            return jsonify({'error': 'order_id and customer_id are required'}), 400
        
        # Step 1: Get customer information from Customer Service
        try:
            customer_response = requests.get(
                f"{CUSTOMER_SERVICE_URL}/api/customers/{customer_id}",
                timeout=5
            )
            
            if customer_response.status_code != 200:
                return jsonify({'error': 'Failed to retrieve customer information'}), 404
            
            customer_data = customer_response.json()
            customer = customer_data['customer']
            customer_name = customer['name']
            customer_email = customer['email']
            customer_phone = customer.get('phone', 'N/A')
            
        except requests.RequestException as e:
            return jsonify({
                'error': 'Failed to connect to Customer Service',
                'details': str(e)
            }), 500
        
        # Step 2: Get order information from Order Service
        try:
            order_response = requests.get(
                f"{ORDER_SERVICE_URL}/api/orders/{order_id}",
                timeout=5
            )
            
            if order_response.status_code != 200:
                order_info = "Order details unavailable"
                order_total = 0
            else:
                order_data = order_response.json()
                order = order_data['order']
                order_total = order.get('total_amount', 0)
                order_info = f"Order Total: ${order_total:.2f}"
            
        except requests.RequestException:
            order_info = "Order details unavailable"
            order_total = 0
        
        # Step 3: Generate notification message
        if notification_type == 'order_confirmation':
            subject = f"Order #{order_id} Confirmed"
            message = f"""
Dear {customer_name},

Your order has been confirmed successfully!

Order ID: {order_id}
{order_info}

Thank you for shopping with us!

Best regards,
E-Commerce Team
            """.strip()
        elif notification_type == 'order_shipped':
            subject = f"Order #{order_id} Shipped"
            message = f"""
Dear {customer_name},

Great news! Your order has been shipped.

Order ID: {order_id}
Estimated delivery: 3-5 business days

Best regards,
E-Commerce Team
            """.strip()
        else:
            subject = f"Notification for Order #{order_id}"
            message = f"Order #{order_id} update for {customer_name}"
        
        # Step 4: Simulate sending notification (console output)
        print("\n" + "=" * 60)
        print("📧 EMAIL NOTIFICATION SENT")
        print("=" * 60)
        print(f"TO: {customer_email}")
        print(f"PHONE: {customer_phone}")
        print(f"SUBJECT: {subject}")
        print("-" * 60)
        print(message)
        print("=" * 60 + "\n")
        
        # Step 5: Log notification to database
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                insert_query = """
                    INSERT INTO notification_log 
                    (order_id, customer_id, notification_type, message, sent_at)
                    VALUES (%s, %s, %s, %s, NOW())
                """
                cursor.execute(insert_query, (order_id, customer_id, notification_type, message))
                conn.commit()
                notification_id = cursor.lastrowid
                
                cursor.close()
                conn.close()
                
            except mysql.connector.Error as err:
                print(f"Failed to log notification: {err}")
                notification_id = None
        else:
            notification_id = None
        
        # Step 6: Return success response
        return jsonify({
            'success': True,
            'message': 'Notification sent successfully',
            'notification_details': {
                'notification_id': notification_id,
                'order_id': order_id,
                'customer_id': customer_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'notification_type': notification_type,
                'sent_at': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@app.route('/api/notifications/history/<int:customer_id>', methods=['GET'])
def get_notification_history(customer_id):
    """Get notification history for a customer"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT * FROM notification_log 
            WHERE customer_id = %s 
            ORDER BY sent_at DESC
        """
        cursor.execute(query, (customer_id,))
        notifications = cursor.fetchall()
        
        # Convert datetime to ISO format
        for notif in notifications:
            notif['sent_at'] = notif['sent_at'].isoformat()
        
        return jsonify({
            'success': True,
            'customer_id': customer_id,
            'notification_count': len(notifications),
            'notifications': notifications
        }), 200
        
    except mysql.connector.Error as err:
        return jsonify({
            'error': 'Database error',
            'details': str(err)
        }), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 NOTIFICATION SERVICE STARTING")
    print("=" * 50)
    print("Port: 5005")
    print("Database: ecommerce_system")
    print("Dependencies:")
    print("  - Customer Service (port 5004)")
    print("  - Order Service (port 5001)")
    print("  - Inventory Service (port 5002)")
    print("Endpoints:")
    print("  - GET  /health")
    print("  - POST /api/notifications/send")
    print("  - GET  /api/notifications/history/<customer_id>")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5005, debug=True)
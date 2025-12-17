import requests
from models import NotificationLog, Customer
from extensions import db
from datetime import datetime

class NotificationService:
    CUSTOMER_SERVICE_URL = "http://localhost:5004/api/customers"
    INVENTORY_SERVICE_URL = "http://localhost:5002/api/inventory"

    @staticmethod
    def send_notification(order_id):
        # 1. Get Customer Info (we need customer_id first, maybe passed in request? 
        # Requirement says "Receive notification requests with order ID")
        # So we need to query Order Service to get customer_id from order_id?
        # Or Notification Service saves logs?
        
        # Requirement Flow: 1. Receive order_id -> 2. GET Customer Service? 
        # But we need customer_id to query Customer Service.
        # Maybe we call Order Service first?  
        # Or "Receive notification requests with order ID" implies we query Order Service for details.
        
        # Let's assume we also get customer_id in the request or we call Order Service.
        # Flow says: "Receive order_id... -> GET Customer Service".
        # I'll add Order Service call to get order details (including customer_id).
        
        # Wait, I don't have Order Service URL here.
        order_service_url = "http://localhost:5001/api/orders"
        
        try:
            # Get Order
            order_resp = requests.get(f"{order_service_url}/{order_id}")
            if order_resp.status_code != 200:
                return False, "Order not found"
            order_data = order_resp.json()
            customer_id = order_data['customer_id']
            
            # Get Customer
            cust_resp = requests.get(f"{NotificationService.CUSTOMER_SERVICE_URL}/{customer_id}")
            customer_email = "unknown@example.com"
            if cust_resp.status_code == 200:
                customer_email = cust_resp.json().get('email')

            # Get Inventory Estimates (Mocking call as per requirements)
            # requests.get(Inventory...)

            # Simulate Email
            message = f"Order #{order_id} Confirmed"
            print(f"EMAIL SENT TO: {customer_email}")
            print(f"Subject: Order #{order_id} Confirmed")
            print(f"Body: {message}")

            # Log
            log = NotificationLog(
                order_id=order_id,
                customer_id=customer_id,
                notification_type='EMAIL',
                message=message
            )
            db.session.add(log)
            db.session.commit()
            return True, "Sent"

        except Exception as e:
            print(f"Notification Error: {e}")
            return False, str(e)
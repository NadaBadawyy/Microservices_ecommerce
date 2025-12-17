# E-Commerce Microservices Backend

This backend consists of 5 independent Python Flask microservices and a MySQL database.

## Prerequisites
- **Python 3.8+**
- **MySQL 8.0+**
- **Database**: Ensure a database named `ecommerce_system` exists and is accessible.

## Setup Instructions

### 1. Install Dependencies
Run the following command in the root folder:
```bash
pip install -r requirements.txt
```

### 2. Database Configuration
1.  Open `config.py`.
2.  Update the `SQLALCHEMY_DATABASE_URI` line with your MySQL credentials:
    ```python
    "mysql+mysqlconnector://<USER>:<PASSWORD>@localhost:3306/ecommerce_system"
    ```

### 3. Initialize Database
### 3. Initialize Database (Migrations)
Run these commands to set up the database schema:
```bash
set FLASK_APP=manage.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
*Note: Since the `migrations` folder is included, you likely only need to run:*
```bash
set FLASK_APP=manage.py
flask db upgrade
```
*If that fails, or if you want to start fresh, delete the `migrations` folder and run the full commands above.*

### 4. Seed Data (Optional)
To add sample products and customers:
```bash
python setup_database.py
```

### 5. Run the Services
**Recommended (Windows):**
Double-click `start_services.bat` to launch all 5 services in separate windows.

**Manual:**
Run each command in a separate terminal:
- `python run_order.py` (Port 5001)
- `python run_inventory.py` (Port 5002)
- `python run_pricing.py` (Port 5003)
- `python run_customer.py` (Port 5004)
- `python run_notification.py` (Port 5005)

## API Integration Guide for Frontend

### 1. Product Inventory
*   **Check Stock**: `GET http://localhost:5002/api/inventory/check/{product_id}`
*   **Response**: `{ "product_id": 1, "quantity_available": 50, "unit_price": 999.99, ... }`

### 2. Pricing & Cart
*   **Calculate Total**: `POST http://localhost:5003/api/pricing/calculate`
*   **Body**:
    ```json
    { "products": [ {"product_id": 1, "quantity": 1} ] }
    ```
*   **Response**: `{ "total_amount": 999.99, "details": [...] }`

### 3. Checkout (Order Placement)
*   **Create Order**: `POST http://localhost:5001/api/orders/create`
*   **Body**:
    ```json
    {
        "customer_id": 1,
        "products": [ {"product_id": 1, "quantity": 1} ],
        "total_amount": 999.99
    }
    ```
*   **Response**: `{ "message": "Order created", "order": { "order_id": 123, ... } }`

### 4. Customer Profile
*   **Get Profile**: `GET http://localhost:5004/api/customers/{customer_id}`
*   **Get Orders**: `GET http://localhost:5004/api/customers/{customer_id}/orders`
*   **Update Loyalty**: `PUT http://localhost:5004/api/customers/{customer_id}/loyalty` (Body: `{ "points": 10 }`)

### 5. Notifications
*   **Send (Triggered by Frontend/Backend)**: `POST http://localhost:5005/api/notifications/send`
*   **Body**: `{ "order_id": 123 }`
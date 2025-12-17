@echo off
echo Starting E-Commerce Microservices...

echo Starting Order Service on port 5001...
start "Order Service (5001)" python run_order.py
timeout /t 1 >nul

echo Starting Inventory Service on port 5002...
start "Inventory Service (5002)" python run_inventory.py
timeout /t 1 >nul

echo Starting Pricing Service on port 5003...
start "Pricing Service (5003)" python run_pricing.py
timeout /t 1 >nul

echo Starting Customer Service on port 5004...
start "Customer Service (5004)" python run_customer.py
timeout /t 1 >nul

echo Starting Notification Service on port 5005...
start "Notification Service (5005)" python run_notification.py
timeout /t 1 >nul

echo All services attempt to start. Please check the new terminal windows for any errors.
pause

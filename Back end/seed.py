from app import create_app
from extensions import db
from Models import Inventory, Pricing, Customer, Notification

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

inventory = [
    Inventory(product_name="Laptop", stock=10),
    Inventory(product_name="Phone", stock=20),
]

pricing = [
    Pricing(product_id=1, price=1000),
    Pricing(product_id=2, price=500),
]

customers = [
    Customer(name="John Doe", email="john@example.com", phone="123-456-7890"),
    Customer(name="Jane Smith", email="jane@example.com", phone="098-765-4321"),
]

notifications = [
    Notification(message="Welcome to our service!", customer_id=1),
    Notification(message="Your order has been shipped.", customer_id=2),
]

db.session.add_all(inventory + pricing + customers + notifications)
db.session.commit()

print("✅ Database seeded successfully")

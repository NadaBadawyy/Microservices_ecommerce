from flask import Flask
from config import Config
from extensions import db
from models import Inventory, PricingRules, TaxRates, Customer, NotificationLog, Order, OrderItem

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def setup_db():
    with app.app_context():
        print("Creating database tables...")
        # db.create_all() # Schema is handled by Flask-Migrate
        # print("Tables created successfully!")
        print("Checking for existing data...")
        
        # Optional: Seed initial data if tables were empty
        if not Inventory.query.first():
            print("Seeding initial data...")
            # Products
            p1 = Inventory(product_name='Laptop', quantity_available=50, unit_price=999.99)
            p2 = Inventory(product_name='Mouse', quantity_available=200, unit_price=29.99)
            p3 = Inventory(product_name='Keyboard', quantity_available=150, unit_price=79.99)
            p4 = Inventory(product_name='Cover', quantity_available=150, unit_price=50.99)
            p5 = Inventory(product_name='Screen', quantity_available=150, unit_price=500.99)
            p6 = Inventory(product_name='TV', quantity_available=150, unit_price=12000.99)


            db.session.add_all([p1, p2, p3, p4, p5, p6])
            
            # Customers
            c1 = Customer(name='Ahmed Hassan', email='ahmed@gmail.com', phone='01012345678', loyalty_points=100)
            c2 = Customer(name='Shahd Essam', email='shahd@gmail.com', phone='01012345638', loyalty_points=100)
            c3 = Customer(name='Dina Salama', email='dina@gmail.com', phone='01012345674', loyalty_points=100)
            c4 = Customer(name='Nada Badawy', email='nada@gmail.com', phone='01112345678', loyalty_points=100)

            db.session.add_all([c1, c2, c3, c4])


            
            # Pricing Rules
            r1 = PricingRules(product_id=1, min_quantity=5, discount_percentage=10.00)
            db.session.add(r1)
            
            db.session.commit()
            print("Initial data seeded.")

if __name__ == "__main__":
    setup_db()

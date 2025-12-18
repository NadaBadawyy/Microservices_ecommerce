from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from extensions import db, migrate
from resources.customer_resource import CustomerResource, CustomerOrdersResource, CustomerLoyaltyResource, CustomerListResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)
    
    # Customer Service Endpoints
    api.add_resource(CustomerResource, "/api/customers/<int:customer_id>")
    api.add_resource(CustomerListResource, "/api/customers")
    api.add_resource(CustomerOrdersResource, "/api/customers/<int:customer_id>/orders")
    api.add_resource(CustomerLoyaltyResource, "/api/customers/<int:customer_id>/loyalty")

    CORS(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5004, debug=True)

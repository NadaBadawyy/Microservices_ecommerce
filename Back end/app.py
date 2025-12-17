from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from extensions import db, migrate

from resources.order_resource import OrderResource
from resources.inventory_resource import InventoryListResource
from resources.pricing_resource import PricingListResource
from resources.customer_resource import CustomerListResource, CustomerResource
from resources.notification_resource import NotificationListResource, NotificationResource, CustomerNotificationsResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)

    api.add_resource(OrderResource, "/orders")
    api.add_resource(InventoryListResource, "/inventory")
    api.add_resource(PricingListResource, "/pricing")
    api.add_resource(CustomerListResource, "/customers")
    api.add_resource(CustomerResource, "/customers/<int:customer_id>")
    api.add_resource(NotificationListResource, "/notifications")
    api.add_resource(NotificationResource, "/notifications/<int:notification_id>")
    api.add_resource(CustomerNotificationsResource, "/customers/<int:customer_id>/notifications")

    CORS(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

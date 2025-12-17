from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from extensions import db, migrate
from resources.inventory_resource import InventoryCheckResource, InventoryUpdateResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)
    
    # Inventory Service Endpoints
    api.add_resource(InventoryCheckResource, "/api/inventory/check/<int:product_id>")
    api.add_resource(InventoryUpdateResource, "/api/inventory/update")
    
    CORS(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5002, debug=True)

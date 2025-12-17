from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from extensions import db, migrate
from resources.pricing_resource import PricingCalculateResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)
    
    # Pricing Service Endpoints
    api.add_resource(PricingCalculateResource, "/api/pricing/calculate")

    CORS(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5003, debug=True)

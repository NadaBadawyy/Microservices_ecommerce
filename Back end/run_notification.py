from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from extensions import db, migrate
from resources.notification_resource import NotificationSendResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)
    
    # Notification Service Endpoint
    api.add_resource(NotificationSendResource, "/api/notifications/send")

    CORS(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5005, debug=True)

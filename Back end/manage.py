from flask import Flask
from flask_migrate import Migrate
from config import Config
from extensions import db
import models  # Import all models so Alembic detects them

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    from flask.cli import FlaskGroup
    cli = FlaskGroup(app)
    cli()

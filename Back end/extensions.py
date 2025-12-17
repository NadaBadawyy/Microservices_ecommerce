from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
# Creates a Flask‑SQLAlchemy extension instance that will manage the database connection 
# and provide the db.Model, db.session, and column types used to define and query models.​
# The actual database configuration (like SQLALCHEMY_DATABASE_URI) is applied later 
# when this instance is bound to a Flask app, usually via db.init_app(app) 
# or by passing app directly when creating it.
migrate = Migrate()
# Creates a Flask‑Migrate extension instance, which integrates Alembic migrations 
# with Flask and Flask‑SQLAlchemy so schema changes can be tracked and applied 
# with commands such as flask db migrate and flask db upgrade.​
# After initialization with migrate.init_app(app, db), it inspects the SQLAlchemy models 
# defined with db and generates migration scripts to upgrade or 
# downgrade the underlying database schema over time
# config.py
import os


# class Config:
#     # SQLALCHEMY_DATABASE_URI = "mysql://[root]:[Dina@1234@localhost:3306/todos_db"
#     SQLALCHEMY_DATABASE_URI = "mysql+mysqlclient://root:Dina%401234@localhost:3306/todos_db"

#     SQLALCHEMY_TRACK_MODIFICATIONS = False
# # tells Flask‑SQLAlchemy not to track every object change and emit signals, 
# # which reduces memory usage and removes the warning about this feature being deprecated 
# # by default
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:Nada%40186@localhost:3306/ecommerce_system"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

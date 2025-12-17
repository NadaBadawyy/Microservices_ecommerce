from extensions import db

class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Inventory {self.product_name}>"

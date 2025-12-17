from extensions import db

class Pricing(db.Model):
    __tablename__ = "pricing"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Pricing {self.product_id}>"

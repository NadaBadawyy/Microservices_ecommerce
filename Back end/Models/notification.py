from extensions import db

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    sent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Notification {self.message[:20]}...>"
from extensions import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Todo {self.title}>"

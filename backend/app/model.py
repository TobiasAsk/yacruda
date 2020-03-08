from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(1024), unique=True, nullable=False)
    title = db.Column(db.String(1024), nullable=False)
    genre = db.Column(db.String(1024), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    last_modified_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Book {self.title}>'

    def __hash__(self):
        return hash((self.title, self.genre))


@db.event.listens_for(Book, 'before_update')
def update_timestamp(mapper, connection, target):
    target.last_modified_at = datetime.utcnow()


def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

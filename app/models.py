from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    thumbnail = db.Column(db.LargeBinary, nullable=False)
    thumbnail_filename = db.Column(db.String(100), nullable=False)
    file = db.Column(db.LargeBinary, nullable=False)
    file_filename = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float)
    purchase_link = db.Column(db.String(200))
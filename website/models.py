from . import db
from flask_login import UserMixin

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe = db.Column(db.String(10000))
    image_path = db.Column(db.String(200))
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    public = db.Column(db.Boolean, default=False)

    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    data = db.relationship('Data', backref='user', lazy=True)

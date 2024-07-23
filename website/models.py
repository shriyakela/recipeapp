from . import db
from flask_login import UserMixin

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('created_groups', lazy=True))  # Changed backref name to 'created_groups'
    recipes = db.relationship('Data', backref='group', lazy=True)
    public = db.Column(db.Boolean, default=False)



class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    recipe = db.Column(db.String(10000))
    image_path = db.Column(db.String(200))
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    public = db.Column(db.Boolean, default=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    recipes = db.relationship('Data', backref='user', lazy=True)
    groups = db.relationship('Group', backref='creator', lazy=True)  # Ensure this matches the 'Group' model

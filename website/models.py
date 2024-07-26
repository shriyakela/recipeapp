from . import db
from flask_login import UserMixin

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('created_groups', lazy=True))
    recipes = db.relationship('Data', backref='group', lazy=True)
    public = db.Column(db.Boolean)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)
    difficulty_level = db.Column(db.String, nullable=False)
    recipe = db.Column(db.String(10000))
    image_path = db.Column(db.String(200))
    ingredients = db.relationship('Ingredient', backref='data', lazy=True)
    instructions = db.Column(db.Text)
    recipe_type = db.Column(db.String, nullable=False)
    public = db.Column(db.Boolean, default=False)
    reviews = db.relationship('Review', backref='recipe', lazy=True)
    comments = db.relationship('Comment', backref='recipe', lazy=True)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    data_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    recipes = db.relationship('Data', backref='user', lazy=True)
    groups = db.relationship('Group', backref='creator', lazy=True)
    shopping_list = db.Column(db.Text, nullable=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thumbs_up = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from website import create_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', r'sqlite:///C:\Users\Shriya.Kela\recipeapp\website\dbScript\app.db')
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# from website.models import *

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

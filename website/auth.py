from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

app = Flask(__name__)
CORS(app)

auth = Blueprint('auth', __name__)
CORS(auth)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid request data.", "category": "error"}), 400

    email = data.get('email')
    password = data.get('password')

    # Add logging to debug incoming data
    app.logger.debug(f"Login attempt with email: {email}")

    if not email or not password:
        return jsonify({"message": "Email and password are required.", "category": "error"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            return jsonify({"email": user.email})
        else:
            return jsonify({"message": "Incorrect password, try again.", "category": "error"}), 401
    else:
        return jsonify({"message": "Email does not exist.", "category": "error"}), 404


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"})

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password1 = data.get('password1')
    password2 = data.get('password2')

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "Email address already exists", "category": "error"}), 409
    elif len(email) < 4:
        return jsonify({"message": "Email must be greater than 3 characters.", "category": "error"}), 400
    elif len(username) < 2:
        return jsonify({"message": "Username must be greater than 1 character.", "category": "error"}), 400
    elif password1 != password2:
        return jsonify({"message": "Passwords don't match.", "category": "error"}), 400
    elif len(password1) < 7:
        return jsonify({"message": "Password must be at least 7 characters.", "category": "error"}), 400
    else:
        new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return jsonify({"email": new_user.email, "username": new_user.username})

        # return jsonify({"message": "Account created successfully!", "category": "success", "user": {"email": new_user.email, "username": new_user.username}})

app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)

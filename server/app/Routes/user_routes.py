# app/Routes/user_routes.py
import logging
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user as flask_login_user, logout_user as flask_logout_user, login_required, current_user
from app.Controllers.user_controller import register_user, login_user, logout_user, generate_token, confirm_token
from app.Middleware.auth import token_required
from app.Models.user import User
from app.Models.site_data import SiteData
from app.extensions import login_manager

# Configure logging
logging.basicConfig(level=logging.INFO)

user_bp = Blueprint('user_bp', __name__)

@login_manager.user_loader
def load_user(user_id):
    logging.info(f"Loading user with ID: {user_id}")
    return User.get(user_id)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("Received data:", data)  # Debug print to check received data

    # Check for required fields
    if 'username' not in data or 'password' not in data:
        missing_fields = []
        if 'username' not in data:
            missing_fields.append("username")
        if 'password' not in data:
            missing_fields.append("password")
        error_message = f"Missing fields: {', '.join(missing_fields)}"
        return jsonify({'error': error_message}), 400
    
    response, status = register_user(data)
    if status == 201:
        logging.info(f"User registered successfully: {data['username']}")
    else:
        logging.warning(f"User registration failed: {response.get('message', 'Unknown error')}")
    return jsonify(response), status



@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user, status = login_user(data)
    if status == 200:
        flask_login_user(user)
        logging.info(f"User logged in successfully: {user.username}")
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        token = generate_token(user)
        logging.info(f"Generated token for user: {token}")
        return jsonify({'message': 'Login successful', 'user': user_data, 'token': token}), status
    else:
        logging.warning(f"Login failed for email: {data['email']}")
        return jsonify(user), status

@user_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    logging.info(f"Attempting to log out user: {current_user.username}")
    response, status = logout_user()
    logging.info(f"User logged out successfully: {current_user.username}")
    return jsonify(response), status

@user_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = confirm_token(token)
    except:
        return jsonify({'message': 'The confirmation link is invalid or has expired.'}), 400

    user = User.get_by_email(email)
    if user.is_verified:
        return jsonify({'message': 'Account already verified. Please log in.'}), 200

    user.is_verified = True
    user.save()
    return jsonify({'message': 'You have confirmed your account. Thanks!'}), 200

@user_bp.route('/home', methods=['GET'])
@token_required
def home(current_user):
    logging.info(f"Accessing home for user: {current_user.username}")
    return jsonify({'message': f'Welcome {current_user.username}'}), 200

@user_bp.route('/saved-sites-preview', methods=['GET'])
@token_required
def get_previews(current_user):
    """ Fetches previews (name and logo) of all sites for the logged-in user. """
    logging.info(f"Fetching previews for user: {current_user.username}")
    try:
        previews = SiteData.get_previews_by_user(current_user.id)
        return jsonify(previews), 200
    except Exception as e:
        logging.error(f"Failed to retrieve site previews: {str(e)}")
        return jsonify({'error': 'Failed to retrieve site previews'}), 500




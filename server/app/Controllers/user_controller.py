# app/Controllers/user_controller.py
import jwt
import logging
import re
from datetime import datetime, timedelta
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.Models.user import User
import bcrypt
from flask import url_for
from flask_login import logout_user as flask_logout_user
from app.extensions import mail
from app.settings import Config

SECRET_KEY = Config.SECRET_KEY

def generate_token(user):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user.id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def generate_email_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt='email-confirm-salt')

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except:
        return False
    return email

def send_verification_email(user):
    token = generate_email_token(user.email)
    msg = Message('Email Verification', sender=Config.MAIL_DEFAULT_SENDER, recipients=[user.email])
    msg.body = f'Please click the link to verify your email: {url_for("user_bp.verify_email", token=token, _external=True)}'
    mail.send(msg)

def validate_password(password):
    """Validates that the password meets the specified criteria."""
    if len(password) < 8:
        return 'Password must be at least 8 characters long.'
    if not re.search(r"[A-Z]", password):
        return 'Password must contain at least one uppercase letter.'
    if not re.search(r"[a-z]", password):
        return 'Password must contain at least one lowercase letter.'
    if not re.search(r"\d", password):
        return 'Password must contain at least one digit.'
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return 'Password must contain at least one special character.'
    return None

def register_user(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    password_error = validate_password(password)
    if password_error:
        return {'message': password_error}, 400
    
    if User.get_by_username(username):
        return {'message': 'Username already exists'}, 400
    
    if User.get_by_email(email):
        return {'message': 'Email already exists'}, 400
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_id = User.create(username=username, email=email, password=hashed_password)
    
    user = User.get_by_email(email)
    send_verification_email(user)
    
    return {'message': 'User created successfully. Please check your email to verify your account.', 'user_id': str(user_id)}, 201

def login_user(data):
    email = data.get('email')
    password = data.get('password')
    
    user = User.get_by_email(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        if not user.is_verified:
            return {'message': 'Email not verified. Please check your email to verify your account.'}, 403
        return user, 200
    else:
        return {'message': 'Invalid email or password'}, 401

def logout_user():
    logging.info("logout_user called")
    flask_logout_user()
    return {'message': 'Logout successful'}, 200

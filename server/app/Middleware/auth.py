from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.Models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'OPTIONS':
            # Allow OPTIONS requests to pass through without authentication
            return f(*args, **kwargs)
        
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.get(data['sub'])
        except Exception as e:
            return jsonify({'message': f'Token is invalid! {str(e)}'}), 401

        return f(current_user, *args, **kwargs)
    
    return decorated

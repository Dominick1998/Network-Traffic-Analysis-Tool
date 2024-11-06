import jwt
from datetime import datetime, timedelta
from backend.models import User
from backend.database import get_db_session
from flask import request, jsonify
from functools import wraps
from config import JWT_SECRET_KEY  # Ensure your config has a secret key

def authenticate_user(username, password):
    """
    Authenticate a user by username and password.
    """
    session = get_db_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and user.password == password:
            return user
    finally:
        session.close()
    return None

def generate_token(user_id, role):
    """
    Generate a JWT token for an authenticated user.
    """
    expiration = datetime.utcnow() + timedelta(hours=2)
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': expiration
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def token_required(f):
    """
    Token-based authentication decorator for route access.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            request.user_id = data['user_id']
            request.role = data['role']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 403
        return f(*args, **kwargs)
    return decorated

def role_required(role):
    """
    Role-based access control decorator for specific user roles.
    """
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if request.role != role:
                return jsonify({'message': 'Access denied: Insufficient privileges!'}), 403
            return f(*args, **kwargs)
        return decorated
    return wrapper

import jwt
from datetime import datetime, timedelta
from backend.models import User
from backend.database import get_db_session
from flask import request, jsonify
from functools import wraps
from config import JWT_SECRET_KEY  # Ensure your config file includes JWT_SECRET_KEY
import bcrypt  # For password hashing and verification

def authenticate_user(username, password):
    """
    Authenticate a user by username and password.
    Args:
        username (str): The username of the user.
        password (str): The plain-text password provided by the user.
    Returns:
        User: Authenticated user object if credentials are correct; None otherwise.
    """
    session = get_db_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
    except Exception as e:
        print(f"Error during user authentication: {e}")
    finally:
        session.close()
    return None

def generate_token(user_id, role):
    """
    Generate a JWT token for an authenticated user.
    Args:
        user_id (int): ID of the authenticated user.
        role (str): Role of the authenticated user.
    Returns:
        str: JWT token.
    """
    expiration = datetime.utcnow() + timedelta(hours=2)
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': expiration
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def decode_token(token):
    """
    Decode a JWT token to extract its payload.
    Args:
        token (str): The JWT token to decode.
    Returns:
        dict: Decoded payload if token is valid; raises an error otherwise.
    """
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])

def token_required(f):
    """
    Token-based authentication decorator for route access.
    Ensures that the user is authenticated via a valid JWT token.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = decode_token(token)
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
    Ensures that the user has the required role to access the route.
    Args:
        role (str): Required role for access.
    """
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if getattr(request, 'role', None) != role:
                return jsonify({'message': 'Access denied: Insufficient privileges!'}), 403
            return f(*args, **kwargs)
        return decorated
    return wrapper

def hash_password(password):
    """
    Hash a plain-text password using bcrypt.
    Args:
        password (str): Plain-text password.
    Returns:
        str: Hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    """
    Verify a plain-text password against a hashed password.
    Args:
        password (str): Plain-text password.
        hashed_password (str): Hashed password from the database.
    Returns:
        bool: True if password matches; False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

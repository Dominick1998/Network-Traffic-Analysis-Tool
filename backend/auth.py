import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "your_secret_key"

def generate_token(user_id, role):
    """
    Generate a JWT token encoding the user's ID and role.

    Args:
        user_id (int): The user's ID.
        role (str): The user's role (e.g., Admin, User).

    Returns:
        str: Encoded JWT token.
    """
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def token_required(func):
    """
    Decorator to ensure a valid token is provided with the request.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 403
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = decoded_token["user_id"]
            request.role = decoded_token["role"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 403
        return func(*args, **kwargs)
    return wrapper

def role_required(role):
    """
    Decorator to ensure the user has the required role to access the route.

    Args:
        role (str): The required role for the route.

    Returns:
        function: The wrapped function with role verification.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.role != role:
                return jsonify({"error": "Unauthorized access"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

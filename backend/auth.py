import jwt
import datetime
from flask import request, jsonify
from functools import wraps

# Secret key for JWT encoding and decoding
SECRET_KEY = "your_secret_key_here"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Token is missing!'}), 403

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 403

        return f(*args, **kwargs)

    return decorated

def generate_token(username):
    """
    Generate a JWT token for a given username.

    Args:
        username (str): The username for which to generate the token.

    Returns:
        str: The generated JWT token.
    """
    token = jwt.encode(
        {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return token

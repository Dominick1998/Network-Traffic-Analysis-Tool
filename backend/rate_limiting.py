from flask import request, jsonify
from functools import wraps
from time import time

# Dictionary to keep track of user request timestamps
user_requests = {}

def rate_limit(max_requests, window_seconds):
    """
    Rate limiting decorator to limit the number of requests per user in a time window.

    Args:
        max_requests (int): Maximum number of requests allowed within the window.
        window_seconds (int): Time window in seconds for rate limiting.

    Returns:
        function: Decorated route function with rate limiting applied.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_ip = request.remote_addr
            current_time = time()

            # Check if user IP exists in user_requests dictionary
            if user_ip not in user_requests:
                user_requests[user_ip] = []

            # Filter out requests older than the time window
            user_requests[user_ip] = [timestamp for timestamp in user_requests[user_ip] if current_time - timestamp < window_seconds]

            # Check if the number of requests exceeds the limit
            if len(user_requests[user_ip]) >= max_requests:
                return jsonify({'error': 'Too many requests, please try again later.'}), 429

            # Add the current request timestamp
            user_requests[user_ip].append(current_time)
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

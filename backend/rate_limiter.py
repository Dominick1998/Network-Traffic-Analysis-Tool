from flask import jsonify, request
from functools import wraps
import time

# Simple in-memory rate limiter storage (for demo purposes, not suitable for production)
RATE_LIMIT_STORAGE = {}

def rate_limit(max_requests, window_seconds):
    """
    Decorator to apply rate limiting to a Flask route.

    Args:
        max_requests (int): Maximum number of requests allowed within the time window.
        window_seconds (int): Time window in seconds.

    Returns:
        function: The decorated function with rate limiting applied.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()

            # Initialize rate limiting info for the client if not present
            if client_ip not in RATE_LIMIT_STORAGE:
                RATE_LIMIT_STORAGE[client_ip] = {
                    'count': 1,
                    'start_time': current_time
                }
            else:
                # Retrieve rate limiting info for the client
                client_data = RATE_LIMIT_STORAGE[client_ip]
                elapsed_time = current_time - client_data['start_time']

                # Reset the count if the time window has passed
                if elapsed_time > window_seconds:
                    client_data['count'] = 1
                    client_data['start_time'] = current_time
                else:
                    # Increment the request count and check if it exceeds the limit
                    client_data['count'] += 1
                    if client_data['count'] > max_requests:
                        return jsonify({'error': 'Too many requests, please try again later.'}), 429

            return f(*args, **kwargs)
        return wrapped
    return decorator

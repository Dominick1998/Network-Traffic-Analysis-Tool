from time import sleep
from flask import jsonify, request
from functools import wraps

# Simple in-memory throttling storage
THROTTLING_STORAGE = {}

def throttle(max_requests, slowdown_seconds):
    """
    Decorator to throttle requests after a certain number of requests.

    Args:
        max_requests (int): Maximum number of requests allowed before throttling is applied.
        slowdown_seconds (int): The number of seconds to delay the response after throttling is triggered.

    Returns:
        function: The decorated function with throttling applied.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            client_ip = request.remote_addr

            # Initialize throttling info for the client if not present
            if client_ip not in THROTTLING_STORAGE:
                THROTTLING_STORAGE[client_ip] = {'count': 1}
            else:
                # Increment the request count and apply throttling if necessary
                THROTTLING_STORAGE[client_ip]['count'] += 1
                if THROTTLING_STORAGE[client_ip]['count'] > max_requests:
                    sleep(slowdown_seconds)
                    THROTTLING_STORAGE[client_ip]['count'] = 0  # Reset after applying the throttle

            return f(*args, **kwargs)
        return wrapped
    return decorator

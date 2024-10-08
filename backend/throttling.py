from flask import request, jsonify
from functools import wraps
from time import sleep

# Dictionary to keep track of user throttling
throttle_users = {}

def throttle(max_requests, slowdown_seconds):
    """
    Throttling decorator to slow down user requests after exceeding the max allowed requests.

    Args:
        max_requests (int): Maximum number of requests before slowdown is applied.
        slowdown_seconds (int): Number of seconds to wait before processing the request.

    Returns:
        function: Decorated route function with throttling applied.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_ip = request.remote_addr

            # Initialize request count for new user IP
            if user_ip not in throttle_users:
                throttle_users[user_ip] = 0

            # Increment request count
            throttle_users[user_ip] += 1

            # Apply throttling if request count exceeds max_requests
            if throttle_users[user_ip] > max_requests:
                sleep(slowdown_seconds)
                throttle_users[user_ip] = 0  # Reset count after slowdown

            return f(*args, **kwargs)
        return wrapped
    return decorator

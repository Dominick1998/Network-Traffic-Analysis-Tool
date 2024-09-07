import logging
from flask import request

# Set up logging
logging.basicConfig(filename='request_logs.log', level=logging.INFO)

def log_request_and_response(app):
    """
    Middleware function to log requests and responses.
    
    Args:
        app (Flask): The Flask app instance to apply the middleware to.
    
    Returns:
        Flask: The Flask app with middleware applied.
    """
    @app.before_request
    def log_request():
        logging.info(f"Request: {request.method} {request.url}")
        logging.info(f"Headers: {request.headers}")
        logging.info(f"Body: {request.get_data(as_text=True)}")

    @app.after_request
    def log_response(response):
        logging.info(f"Response: {response.status_code} {response.get_data(as_text=True)}")
        return response

    return app

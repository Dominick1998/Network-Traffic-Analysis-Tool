import os
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'server.log')

# Ensure the log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def setup_log_rotation():
    """
    Set up log rotation for main application logs.
    """
    handler = RotatingFileHandler("app.log", maxBytes=5*1024*1024, backupCount=5)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Log rotation setup completed.")

# Call setup to initialize log rotation when the app starts
setup_log_rotation()

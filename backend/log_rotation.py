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
    Setup log rotation to limit log file size and maintain log history.
    Rotates logs after they reach a certain size.
    """
    # Set up log rotation (5MB per file, keep 5 backups)
    handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5)
    logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    logging.info('Log rotation setup complete.')

# Call setup to initialize log rotation when the app starts
setup_log_rotation()

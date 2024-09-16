import logging
from logging.handlers import RotatingFileHandler

def setup_log_rotation(log_file='request_logs.log', max_bytes=5000000, backup_count=5):
    """
    Set up log rotation to ensure logs don't grow too large.

    Args:
        log_file (str): The file to store logs.
        max_bytes (int): Maximum size of the log file in bytes before rotation.
        backup_count (int): Number of backup log files to keep.
    """
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger().addHandler(handler)

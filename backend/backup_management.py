import os
import shutil
import logging
from datetime import datetime

# Define the directory for storing backups
BACKUP_DIR = 'backups'
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def create_backup(database_path):
    """
    Create a backup of the current database by copying the database file.

    Args:
        database_path (str): Path to the database file.

    Returns:
        dict: Success or failure message.
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    backup_filename = f"backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    try:
        shutil.copy(database_path, backup_path)
        logging.info(f"Backup created successfully at {backup_path}")
        return {'message': f"Backup created successfully at {backup_path}"}
    except Exception as e:
        logging.error(f"Failed to create backup: {e}")
        return {'error': f"Failed to create backup: {e}"}

def restore_backup(backup_filename, database_path):
    """
    Restore the database from a backup file.

    Args:
        backup_filename (str): Name of the backup file.
        database_path (str): Path to the current database file.

    Returns:
        dict: Success or failure message.
    """
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    if not os.path.exists(backup_path):
        logging.error(f"Backup file {backup_filename} does not exist.")
        return {'error': 'Backup file does not exist.'}

    try:
        shutil.copy(backup_path, database_path)
        logging.info(f"Backup restored successfully from {backup_path}")
        return {'message': 'Backup restored successfully.'}
    except Exception as e:
        logging.error(f"Failed to restore backup: {e}")
        return {'error': f"Failed to restore backup: {e}"}

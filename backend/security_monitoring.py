import os
import shutil
from datetime import datetime

BACKUP_DIR = 'backups'

def create_backup(database_path):
    """
    Create a backup of the current database by copying the database file.

    Args:
        database_path (str): Path to the database file.

    Returns:
        dict: Success or failure message.
    """
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    backup_filename = f"backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    try:
        shutil.copy(database_path, backup_path)
        return {'message': f"Backup created successfully at {backup_path}"}
    except Exception as e:
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
        return {'error': 'Backup file does not exist.'}

    try:
        shutil.copy(backup_path, database_path)
        return {'message': 'Backup restored successfully.'}
    except Exception as e:
        return {'error': f"Failed to restore backup: {e}"}

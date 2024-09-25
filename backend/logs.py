import os
from flask import jsonify, send_file

LOG_FILE = 'request_logs.log'

def get_logs():
    """
    Serve the log file content for viewing.

    Returns:
        JSON response with logs content or an error if the file is not found.
    """
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log_file:
            logs = log_file.read()
        return jsonify({'logs': logs}), 200
    else:
        return jsonify({'error': 'Log file not found'}), 404

def download_logs():
    """
    Provide the log file for download.

    Returns:
        A Flask response that initiates a file download.
    """
    if os.path.exists(LOG_FILE):
        return send_file(LOG_FILE, as_attachment=True, attachment_filename='server_logs.log')
    else:
        return jsonify({'error': 'Log file not found'}), 404

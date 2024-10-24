notifications = []

def add_notification(notification):
    """
    Add a new notification to the system.

    Args:
        notification (dict): A dictionary with notification details (e.g., type, message).
    
    Returns:
        dict: Success message.
    """
    notifications.append(notification)
    return {'message': 'Notification added successfully.'}

def get_notifications():
    """
    Retrieve all notifications.

    Returns:
        list: List of notifications.
    """
    return notifications

def clear_notifications():
    """
    Clear all notifications.

    Returns:
        dict: Success message.
    """
    notifications.clear()
    return {'message': 'All notifications cleared.'}

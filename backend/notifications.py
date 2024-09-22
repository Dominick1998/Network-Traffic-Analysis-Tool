from backend.email_notifications import send_email_notification

def send_admin_notification(subject, message):
    """
    Send a notification to the admin via email.

    Args:
        subject (str): The subject of the notification.
        message (str): The message body of the notification.
    """
    try:
        send_email_notification(
            to_email='admin@example.com',
            subject=subject,
            message=message
        )
        print(f"Notification sent: {subject}")
    except Exception as e:
        print(f"Error sending notification: {e}")

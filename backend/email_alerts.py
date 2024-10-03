import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.database import get_db_session
from backend.models import Alert

def send_custom_alert_email(alert_name, condition, action):
    """
    Send an email when a custom alert is triggered.

    Args:
        alert_name (str): Name of the alert.
        condition (str): Condition that triggered the alert.
        action (str): The action defined for the alert.
    """
    sender_email = "admin@example.com"
    receiver_email = "recipient@example.com"
    password = "your_password"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Alert Triggered: {alert_name}"

    # Create the body of the email
    body = f"""
    The following alert was triggered based on your defined conditions:
    
    Alert Name: {alert_name}
    Condition: {condition}
    Action Taken: {action}
    
    Please take the necessary steps to address this issue.
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Send the email
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"Alert email sent to {receiver_email}.")
    except Exception as e:
        print(f"Failed to send email: {e}")

import smtplib
from email.mime.text import MIMEText

def send_email_notification(to_email, subject, message):
    """
    Send an email notification.

    Args:
        to_email (str): Recipient email address.
        subject (str): Subject of the email.
        message (str): Body of the email.
    """
    sender_email = "your-email@example.com"
    smtp_server = "smtp.example.com"
    smtp_port = 587
    smtp_username = "your-username"
    smtp_password = "your-password"

    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, to_email, msg.as_string())

        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

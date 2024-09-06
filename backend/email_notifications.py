import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration (replace with your actual credentials)
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_USERNAME = 'your-email@example.com'
EMAIL_PASSWORD = 'your-email-password'
EMAIL_FROM = 'your-email@example.com'

def send_email_notification(to_email, subject, message):
    """
    Send an email notification to the specified email address.

    Args:
        to_email (str): The recipient's email address.
        subject (str): The subject of the email.
        message (str): The message body of the email.

    Returns:
        None
    """
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the message body
        msg.attach(MIMEText(message, 'plain'))

        # Set up the SMTP server
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

        # Send the email
        server.sendmail(EMAIL_FROM, to_email, msg.as_string())
        server.quit()

        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

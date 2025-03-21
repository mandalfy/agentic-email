import smtplib
from email.mime.text import MIMEText

def send_email(sender, password, to, subject, body):
    """Send an email using SMTP."""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
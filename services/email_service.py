import smtplib
from email.message import EmailMessage
from config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, RECRUITER_EMAIL

def send_email(to, subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

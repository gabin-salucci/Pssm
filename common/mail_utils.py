import smtplib
from email.mime.text import MIMEText

from config.config import MAIL

def send_mail(subject, body, to=None):
    recipient = to or MAIL["admin_recipient"]

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = MAIL["sender"]
    msg["To"] = recipient

    with smtplib.SMTP(MAIL["smtp_server"], MAIL["smtp_port"]) as server:
        server.starttls()
        server.login(MAIL["sender"], MAIL["app_password"])
        server.sendmail(MAIL["sender"], [recipient], msg.as_string())

# email_utils.py
import smtplib
from email.mime.text import MIMEText

def send_email_alert(subject, body, to_email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = "mmohanty335@gmail.com"
    password = "your_app_password_here"  # 🔒 use GitHub Secret instead

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, [to_email], msg.as_string())

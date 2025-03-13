import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password


    async def send_email(self, to_email: str, subject: str, body: str):
        if os.getenv("USE_SIMULATED_EMAIL").lower() == "true":
            return
        msg = MIMEMultipart()
        msg["From"] = f"Credit simulator <{self.username}>"
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.username, to_email, text)
            server.quit()
            logger.info("Email sent to %s", to_email)
        except Exception as e:
            logger.error("Failed to send email: %s", e)
            raise



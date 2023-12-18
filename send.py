import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv('ACC_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

def _email(email_send,subject,body):
    password = os.getenv('EMAIL_PASS')
    email_user = "amogh.out@outlook.com"
    email_password = password
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    text = msg.as_string()
    server = smtplib.SMTP("smtp.outlook.com", 587)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, email_send, text)
    server.quit()

def _msg(ph,otp):
    b=f'Your zomapes otp for login is {otp}'
    message = client.messages.create(
    from_='+12164382762',
    body=b,
    to=ph
    )

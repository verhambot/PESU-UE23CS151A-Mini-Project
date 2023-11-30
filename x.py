# import mysql.connector as sql

# sqlc = sql.connect(
#     host = 'localhost',
#     user = 'root',
#     password = 'Amogh2004',
#     database = 'zomapes'
# )

# cur=sqlc.cursor()
# cur.execute(f'update carts set quantity=2 where srn="PES1UG23AM043" and food="Chicken Biryani;"')
# sqlc.commit()


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
def send_email():
    email_user = "amogh.out@outlook.com"
    email_password = "5f3Ddf0c!!!904"
    email_send = "amogh.e.m7@gmail.com"
    subject = "Hello world"
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["Subject"] = subject
    body = "test"
    msg.attach(MIMEText(body, "plain"))
    text = msg.as_string()
    server = smtplib.SMTP("smtp.outlook.com", 587)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, email_send, text)
    server.quit()
    print("done")

send_email()
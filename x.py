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


# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# def send_email():
#     email_user = "amogh.out@outlook.com"
#     email_password = "5f3Ddf0c!!!904"
#     email_send = "amogh.e.m7@gmail.com"
#     subject = "Hello world"
#     msg = MIMEMultipart()
#     msg["From"] = email_user
#     msg["Subject"] = subject
#     body = "test"
#     msg.attach(MIMEText(body, "plain"))
#     text = msg.as_string()
#     server = smtplib.SMTP("smtp.outlook.com", 587)
#     server.starttls()
#     server.login(email_user, email_password)
#     server.sendmail(email_user, email_send, text)
#     server.quit()
#     print("done")

# send_email()



# import random
# import hashlib
# def genotp(ph=123):
#     gotp = random.randint(100000, 999999)
#     # message = client.messages.create(
#     #     from_='+12164382762',
#     #     body=f'Your zomapes otp is {gotp}',
#     #     to=ph
#     # )
#     sha256 = hashlib.sha256()
#     sha256.update(str(gotp).encode())
#     string_hash = sha256.hexdigest()
#     return string_hash
# print(genotp())

# from flask import Flask, render_template, session
# from flask_session import Session

# app = Flask(__name__)

# # Configure session to use filesystem (you can choose other backends like Redis, etc.)
# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)

# @app.route('/page1')
# def page1():
#     session['my_data'] = 'Hello from Page 1!'
#     return render_template('page1.html')

# @app.route('/page2')
# def page2():
#     my_data = session.pop('my_data', None)
#     return render_template('page2.html', my_data=my_data)


print('1234'.isdigit())

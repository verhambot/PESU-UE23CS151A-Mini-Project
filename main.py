import flask
from flask import Flask, request, render_template, redirect, url_for
from twilio.rest import Client
import random
import mysql.connector as sql
import hashlib

app = Flask(__name__)
sqlc = sql.connect(
    host = 'localhost',
    user = 'root',
    password = 'Amogh2004',
    database = 'zomapes'
)
cur=sqlc.cursor()
account_sid = 'ACe93a1e1c711c40d0b8ab76679e07fd2e'
auth_token = '916dfbab7bb18282fabe634459ae7635'
client = Client(account_sid, auth_token)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session={}
        srn = request.form.get('srn')
        hashedsrn=hash256(srn)
        cur.execute(f'select phone from log1 where SRN="{hashedsrn}";')
        ph=cur.fetchone()
        if ph:
            gotp = genotp(ph)
            session[1]=gotp
            return redirect(url_for('home',session=session))
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    session = request.args.get('session')
    if session is None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        session = request.args.get('session')
        if entered_otp==session[4:10]:
            return render_template('home.html', success=True)
    return render_template('home.html', success=False)

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        cod=request.form.get('pcode')
        srn=request.form.get('srn')
        phone=request.form.get('phone')
        phno=cod+phone
        hashedsrn=hash256(srn)
        cur.execute(f"insert into log1 values('{hashedsrn}','{phno}')")
        sqlc.commit()
        return 'registered'
    return render_template('register.html',data=[{'code':'+91'}, {'code':'+619'}, {'code':'+69'}])

def genotp(ph):
    gotp = random.randint(100000, 999999)
    message = client.messages.create(
        from_='+12164382762',
        body=f'Your zomapes otp is {gotp}',
        to=ph
    )
    print(gotp)
    return gotp

def validate_otp(eotp, genotp):
    return eotp == genotp

def hash256(string1):
    hashed=hashlib.sha256(string1.encode()).hexdigest()
    return(hashed)

if __name__ == '__main__':
    app.run(debug=True)

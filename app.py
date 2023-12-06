from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from twilio.rest import Client
import random
import mysql.connector as sql
import hashlib
import os
from dotenv import load_dotenv
from flask_session import Session
load_dotenv()

account_sid = os.getenv('ACC_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
sqlc = sql.connect(
    host = 'localhost',
    user = 'root',
    password = 'Amogh2004',
    database = 'zomapes'
)
cur=sqlc.cursor(buffered=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        srn = request.form.get('srn')
        cur.execute(f'select phone from log1 where SRN="{srn}";')
        ph=cur.fetchone()
        if ph:
            session['srn']=srn
            session['gotp']=genotp(ph)
            session['logged_in']=False
            return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    srn = session.get('srn')
    gotp = session.get('gotp')
    if gotp is None or srn is None:
        return redirect(url_for('index'))
    if 'cart' in request.form:
        session['srn']=srn
        return redirect(url_for('cart'))
    if request.method == 'POST' or session['logged_in']:
        if 'otp' in request.form or session['logged_in']:
            entered_otp = request.form.get('otp')
            if 'backfromcart' in request.form:
                entered_otp=gotp
            cur.execute(f'select wallet from log1 where SRN="{srn}";')
            wallet=cur.fetchone()[0]
            if validate_otp(entered_otp,gotp) or session['logged_in']:
                session['logged_in']=True
                cur.execute("select Food,Price from zomamenu;")
                data=[]
                x=cur.fetchall()
                for i in x:
                    di1={}
                    di1['food']=i[0]
                    di1['price']=i[1]
                    data.append(di1)
                cur.execute(f"select * from orders where srn='{srn}';")
                x=cur.fetchall()
                orders=[]
                for i in x:
                    di1={}
                    di1['orderno']=i[0]
                    di1['order']=i[1]
                    di1['transactionid']=i[3]
                    di1['status']=i[4]
                    di1['quantity']=i[5]
                    orders.append(di1)
                cur.execute(f"select * from carts where srn='{srn}';")
                x=cur.fetchall()
                cart=[]
                for i in x:
                    di1={}
                    di1['food']=i[0]
                    di1['price']=i[1]
                    di1['quantity']=i[2]
                    cart.append(di1)
                cur.execute(f"delete from carts where srn='{srn}';")
                sqlc.commit()
                return render_template('home.html', data=data, orders=orders, wallet=wallet, cart=cart, srn=srn, success=True)
    return render_template('home.html', success=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cod=request.form.get('pcode')
        srn=request.form.get('srn')
        phone=request.form.get('phone')
        phno=cod+phone
        if srn and phone:
            cur.execute(f"insert into log1 values('{srn}','{phno}')")
            sqlc.commit()
            return 'registered'
    return render_template('register.html',data=[{'code':'+91'}, {'code':'+619'}, {'code':'+69'}])

@app.route('/cartAdd', methods=['POST'])
def cartAdd():
    quant = request.get_json()
    if quant[2]>1:
        cur.execute(f'update carts set quantity={quant[2]} where srn="{quant[3]}" and food="{quant[0]}";')
    else:
        cur.execute(f'insert into carts values{tuple(quant)};')
    sqlc.commit()
    return 'added'

@app.route('/cartSub', methods=['POST'])
def cartSub():
    quant = request.get_json()
    if quant[2]>0:
        cur.execute(f'update carts set quantity={quant[2]} where srn="{quant[3]}" and food="{quant[0]}";')
    elif quant[2]==0:
        cur.execute(f'delete from carts where srn="{quant[3]}" and food="{quant[0]}";')
    sqlc.commit()
    return 'removed'

@app.route('/cart',methods=['GET','POST'])
def cart():
    srn=session.get('srn')
    if srn:
        cur.execute(f'select * from carts where srn="{srn}";')
        cart=[]
        x=cur.fetchall()
        for i in x:
            di1={}
            di1['food']=i[0]
            di1['price']=i[1]
            di1['quantity']=i[2]
            cart.append(di1)
        return render_template('cart.html', cart=cart,srn=srn)
    else:
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

def genotp(ph):
    gotp = random.randint(100000, 999999)
    # message = client.messages.create(
    #     from_='+12164382762',
    #     body=f'Your zomapes otp is {gotp}',
    #     to=ph
    # )
    sha256 = hashlib.sha256()
    sha256.update(str(gotp).encode())
    string_hash = sha256.hexdigest()
    print(gotp)
    return string_hash

def validate_otp(eotp, genotp):
    sha256 = hashlib.sha256()
    sha256.update(str(eotp).encode())
    ehotp = sha256.hexdigest()
    print(ehotp)
    return ehotp == genotp or eotp==genotp

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

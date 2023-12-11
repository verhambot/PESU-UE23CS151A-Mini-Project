from flask import Flask, request, render_template, redirect, url_for, session
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
            session['gotp']=genotp(1)
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
            wallet=round(cur.fetchone()[0],2)
            session['wallet']=wallet
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
                    di1['transactionid']=i[3][-6::]
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
            cur.execute(f"insert into log1 values('{srn}','{phno}',0);")
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
    
@app.route('/receipt',methods=['POST'])
def receipt():
    srn=session.get('srn')
    # if request.method=='POST':
    wallbal=session.get('wallet')
    print(wallbal)
    cur.execute(f'select sum(price) from carts where srn="{srn}";')
    grandtotal=cur.fetchone()[0]
    print(grandtotal)
    grandtotal=round(1.18*grandtotal,2)

    if wallbal>=grandtotal:
        cur.execute(f'select * from carts where srn="{srn}";')
        cart=cur.fetchall()
        cur.execute('select orderno from orders')
        currorder=cur.fetchall()[-1][0]+1
        tID=createTransID(srn,grandtotal,currorder)
        for i in cart:
            cur.execute(f'insert into orders values({currorder},"{i[0]}",{i[1]},"{tID}","paid",{i[2]},"{srn}");')
        wallbal-=grandtotal
        cur.execute(f'update log1 set wallet={wallbal} where srn="{srn}";')
        orderotp=genotp(3)
        cur.execute(f'insert into adminmanageorders values({currorder},"{orderotp[1]}","{srn}");')
        sqlc.commit()
        return redirect(url_for('uorders'))
    else:
        return redirect(url_for('addmoni'))

@app.route('/uorders',methods=['GET','POST'])
def uorders():
    srn=session.get('srn')
    cur.execute(f'select * from adminmanageorders where srn="{srn}";')
    userorders=cur.fetchall()
    passOrders=[]
    orderindex=[]
    for i in userorders:
        data={}
        data['orderno']=i[0]
        orderindex.append(i[0])
        data['otp']=i[1]
        passOrders.append(data)
    if request.method=='POST' and 'orderotp' in request.form:
        selectOrder=request.form.get('orderno')
        oi=orderindex.index(int(selectOrder))
        otpSelected=request.form.get('orderotp')
        diForOtp=passOrders[oi]
        checkotp=diForOtp['otp']
        if validate_otp(otpSelected,checkotp):
            cur.execute(f'delete from adminmanageorders where orderno={selectOrder};')
            cur.execute(f'update orders set status="collected" where srn="{srn}" and orderno={selectOrder};')
            sqlc.commit()
            return redirect(url_for('uorders'))
        return redirect(url_for('uorders'))
    return render_template('uorders.html',passOrders=passOrders)

@app.route('/addmoni',methods=['GET','POST'])
def addmoni():
    srn=session.get('srn')
    if request.method=='POST':
        amt=float(request.form.get('money'))
        status=request.form.get('status')
        if status:
            cur.execute(f'update log1 set wallet={amt} where SRN="{srn}";')
            return 'added'
    return render_template('addmoni.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

def genotp(type):
    gotp = random.randint(100000, 999999)
    sha256 = hashlib.sha256()
    sha256.update(str(gotp).encode())
    string_hash = sha256.hexdigest()
    print(gotp)
    if type==1:
        return string_hash
    elif type==2:
        return gotp
    elif type==3:
        return [gotp,string_hash]
    else:
        return string_hash

def send_msg(ph,otp,reason):
    b=''
    if reason==1:
        b=f'Your zomapes otp for login is {otp}'
    message = client.messages.create(
        from_='+12164382762',
        body=b,
        to=ph
    )

def validate_otp(eotp, genotp):
    sha256 = hashlib.sha256()
    sha256.update(str(eotp).encode())
    ehotp = sha256.hexdigest()
    return ehotp == genotp or eotp == genotp

def createTransID(srn,moni,order):
    s=str(srn)+str(moni)+str(order)
    sha256 = hashlib.sha256()
    sha256.update(s.encode())
    transID = sha256.hexdigest()
    return transID

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

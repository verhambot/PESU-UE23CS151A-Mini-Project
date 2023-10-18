from flask import Flask, render_template, redirect, url_for, request
app=Flask(__name__)

users=["arnav","amogh"]

@app.route("/")
def home():
    error = None
    return render_template('first.html',error=error)
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] !="admin" or request.form['password'] != 'admin':
            error = 'wrong username or password combination'
        else:
            return redirect(url_for('user_page'))
    return render_template('login.html', error=error)
@app.route("/user")
def user_page():
    return "<h1>Logged in sucessfully</h1>"
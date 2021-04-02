from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for, session
import os
import db_manager


app = Flask(__name__)
app.secret_key = (os.urandom(16))


@app.route("/")
def index_page():
    return render_template("main_page.html")


@app.route("/registration")
def registration_page():
    return render_template("registration_page.html")


@app.route('/registration', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for("display_questions_list"))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if db_manager.register_user(username, password, submission_time) is False:
            print('NOT REGISTERED')
        db_manager.register_user(username, password, submission_time)
        return redirect(url_for('login'))
    return render_template('registration_page.html')


@app.route("/login")
def login_page():
    return render_template("login_page.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('display_questions_list'))
    if request.method == 'POST':
        username = request.form.get('username')
        typed_password = request.form.get('password')
        user = db_manager.check_user(username)
        if user and db_manager.verify_password(typed_password, user['password']):
            session['user_id'] = user['id']
            session['username'] = username
            print('LOGGED IN')
            return redirect('/')
        else:
            print('INVALID USERNAME OR PASSWORD')
    return render_template('login_page.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(
        host='localhost',
        port=5000,
        debug=True,
    )

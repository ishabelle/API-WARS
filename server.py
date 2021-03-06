from datetime import datetime

import flask
from flask import Flask, render_template, redirect, request, url_for, session, flash, jsonify
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
        return redirect(url_for("index_page"))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if username == '' or password == '':
            flash('Please, fill in both fields.')
        elif db_manager.register_user(username, password, submission_time) is False:
            flash('Username already exists, please choose another one!')
        else:
            db_manager.register_user(username, password, submission_time)
            flash('Successful registration. Log in to continue.')
            return redirect(url_for('login_page'))
    return render_template('registration_page.html')


@app.route("/login")
def login_page():
    return render_template("login_page.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index_page'))
    if request.method == 'POST':
        username = request.form.get('username')
        typed_password = request.form.get('password')
        user = db_manager.check_user(username)
        if user and db_manager.verify_password(typed_password, user['password']):
            session['user_id'] = user['id']
            session['username'] = username
            flash('Login successful!')
            return redirect('/')
        else:
            flash('Wrong username or password. Please try again.')
    return render_template('login_page.html')


@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('username', None)
    flash("You are logged out!")
    return redirect(url_for('index_page'))


@app.route('/api/vote-planets', methods=['GET', 'POST'])
def vote_planets():
    json_data = flask.request.json
    planet_id = json_data['planet_id']
    planet_name = json_data['planet_name']
    user_id = session['user_id']
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_manager.vote_planet_by_planet_name(planet_id, planet_name, user_id, submission_time)
    flash('Voted on planet ' + planet_name + ' successfully')
    return jsonify({'success': True})


@app.route('/api/get-planets-votes')
def get_planets_votes():
    statistics = db_manager.get_vote_statistics()
    return jsonify(statistics)


if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(
        host='localhost',
        port=5000,
        debug=True,
    )

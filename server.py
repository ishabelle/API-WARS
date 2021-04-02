from flask import Flask, render_template, redirect, request, url_for, flash
import os

import db_manager
import password_generator


app = Flask(__name__)
app.secret_key = (os.urandom(16))


@app.route("/")
def index_page():
    return render_template("main_page.html")


@app.route("/registration")
def registration_page():
    return render_template("registration_page.html")


@app.route("/registration", methods=["POST"])
def register_new_user():
    new_user = request.form.to_dict()
    hashed_password = password_generator.generate_hash_password(request.form.get('password'))
    new_user['password'] = hashed_password
    if db_manager.add_user(new_user) is False:
        return redirect(url_for('registration_page'))
    db_manager.add_user(new_user)
    print("User registered")
    return redirect(url_for('index_page'))


@app.route("/login")
def login_page():
    return render_template("login_page.html")


@app.route("/login", methods=["POST"])
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')
    user_details = db_manager.get_user_details(username)
    if not user_details:
        flash("INVALID USERNAME OR PASSWORD")
        return redirect(url_for('login_page'))
    else:
        verified_password = password_generator.check_hash_password(user_details['password'], password)
    if not verified_password:
        flash("INVALID PASSWORD")
    else:
        return redirect(url_for('index_page'))


if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(
        host='localhost',
        port=5000,
        debug=True,
    )

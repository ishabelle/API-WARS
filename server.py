from flask import Flask, render_template, redirect, request, url_for
import db_common
import db_manager
import password_generator


app = Flask(__name__)


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


if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(
        host='localhost',
        port=5000,
        debug=True,
    )

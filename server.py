from flask import Flask, render_template, redirect, url_for, session, request


app = Flask('__name__')


@app.route('/')
def main_page():
    return render_template('main_page.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(
        host='localhost',
        port=5000,
        debug=True,
    )

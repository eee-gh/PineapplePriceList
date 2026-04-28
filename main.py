from flask import Flask
from flask import Flask, render_template, redirect, make_response, jsonify
from data import db_session
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)


@app.route('/')
def index():
    return render_template('index.html', title='Главная')


if __name__ == '__main__':
    db_session.global_init("db/base.db")
    app.run(port=8080, host='127.0.0.1', debug=True)

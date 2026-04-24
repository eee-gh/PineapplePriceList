from flask import Flask
from flask import Flask, render_template, redirect, make_response, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title='Главная')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)

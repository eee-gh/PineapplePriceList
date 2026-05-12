import base64
import datetime
import os

from flask import Flask
from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from sqlalchemy import func
from werkzeug.utils import secure_filename

from data import db_session, boards
from data.users import User
from data.boards import Board
from data.posts import Post
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from forms.treads import TreadForm
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(name):
    db_sess = db_session.create_session()
    return db_sess.get(User, name)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    b = [i[0] for i in db_sess.query(Board.name).all()]
    return render_template('index.html', title='Главная', boards=b)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/board')
def board_list():
    return render_template('boards.html', title='Доски')


@app.route('/user')
def user_list():
    return render_template('users.html', title='Пользователи')


@app.route('/board/<board>')
def show_board(board):
    db_sess = db_session.create_session()
    data = db_sess.query(Board).filter(Board.name == board).first()
    return render_template('board.html', title=board, name=data.name,
                           descr=data.description, pic=data.picture, cr_dt=data.created_date, cr_by=data.created_by,
                           posts=[])


@app.route('/user/<user>')
def user_profile(user):
    return f'Пользователь: {user}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Пост №: {post_id}'


@app.route('/board/<board>/new', methods=['GET', 'POST'])
@login_required
def create_tread(board):
    form = TreadForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        tread = Post()
        tread.reply_to = -1
        nid = db_sess.query(func.max(Post.id)).scalar()
        if nid is None: nid = 0
        nid += 1
        tread.id = nid
        tread.content = form.content.data
        tread.created_date = datetime.datetime.now()
        tread.board_on = board
        tread.created_by = current_user.name

        if form.image.data:
            f = form.image.data
            tread.image = f.read()

        if form.file.data:
            f = form.file.data
            filename = secure_filename(f.filename)
            f.save(os.path.join('uploads', filename))
            tread.file = filename

        db_sess.add(tread)
        db_sess.commit()
        return redirect('/')
    return render_template('new_tread.html', title='Создание треда', form=form)


if __name__ == '__main__':
    db_session.global_init("db/base.db")
    db_sess = db_session.create_session()
    app.run(port=8080, host='127.0.0.1', debug=True)

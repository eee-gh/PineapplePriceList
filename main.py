import base64
import datetime
import os

from flask import Flask, render_template, redirect, send_from_directory, request, abort
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from markupsafe import escape
from werkzeug.utils import secure_filename

from data import db_session
from data.users import User
from data.boards import Board
from data.posts import Post
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from forms.threads import ThreadForm
from forms.replies import ReplyForm
from forms.user import UserForm
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
login_manager = LoginManager()
login_manager.init_app(app)
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')


def format_greentext(text):
    if not text:
        return ''
    safe_text = str(escape(text))
    lines = safe_text.split('\n')
    formatted_lines = []
    for line in lines:
        if line.startswith('&gt;'):
            formatted_lines.append(f'<span class="greentext">{line}</span>')
        else:
            formatted_lines.append(line)
    return '\n'.join(formatted_lines)


app.jinja_env.filters['greentext'] = format_greentext


@login_manager.user_loader
def load_user(name):
    return db_sess.get(User, name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
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
    return redirect('/')


@app.route('/uploads/<filename>')
def download_file(filename):
    custom_name = request.args.get('name', filename)
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True, download_name=custom_name)


@app.route('/board')
@app.route('/board/')
@app.route('/user')
@app.route('/user/')
@app.route('/post')
@app.route('/post/')
def rd():
    return redirect('/')


@app.route('/')
def index():
    b = [i.name for i in db_sess.query(Board.name).all()]
    return render_template('index.html', title='Главная', boards=b)


@app.route('/board/<board>')
@app.route('/board/<board>/')
@app.route('/board/<board>/<int:page>')
def show_board(board, page=1):
    data = db_sess.query(Board).filter(Board.name == board).first()
    if data is None:
        return abort(404)
    d = {'name': data.name, 'descr': data.description}
    threads = (db_sess.query(Post).filter(Post.reply_to == -1, Post.board_on == board)
               .order_by(Post.created_date.desc())).limit(10).offset(10 * (page - 1)).all()
    f = True if (db_sess.query(Post).filter(Post.reply_to == -1, Post.board_on == board)
                 .order_by(Post.created_date.desc())).limit(10).offset(10 * (page)).all() else False
    t = []
    for i in threads:
        a = {'thread': {'id': i.id, 'reply_to': -1, 'content': i.content,
                        'image': base64.b64encode(i.image).decode('utf-8') if i.image else None, 'file': i.file,
                        'created_date': datetime.datetime.fromtimestamp(i.created_date / 1000.0),
                        'board_on': i.board_on, 'created_by': i.created_by},
             'replies': []}
        replies = db_sess.query(Post).filter(Post.reply_to == i.id).order_by(Post.created_date.desc()).limit(3).all()
        for r in replies:
            a['replies'].append({'id': r.id, 'reply_to': r.reply_to, 'content': r.content,
                                 'image': base64.b64encode(r.image).decode('utf-8') if r.image else None,
                                 'file': r.file,
                                 'created_date': datetime.datetime.fromtimestamp(i.created_date / 1000.0),
                                 'board_on': r.board_on, 'created_by': r.created_by})
        t.append(a)

    return render_template('board.html', title=board, d=d, threads=t, page=page, next_p=f)


@app.route('/user/<user>')
@app.route('/user/<user>/')
def user_profile(user):
    usr = db_sess.query(User).filter(User.name == user).first()
    if usr is None:
        abort(404)
    u = {'name': usr.name, 'descr': usr.description,
         'pic': base64.b64encode(usr.picture).decode('utf-8') if usr.picture else None}

    return render_template('user.html', title=user, u=u)


@app.route('/post/<int:post_id>')
@app.route('/post/<int:post_id>/')
def show_post(post_id):
    post = db_sess.query(Post).filter(Post.id == post_id).first()
    if post is None:
        abort(404)
    d = {'id': post.id, 'reply_to': post.reply_to, 'content': post.content,
         'image': base64.b64encode(post.image).decode('utf-8') if post.image else None, 'file': post.file,
         'created_date': datetime.datetime.fromtimestamp(post.created_date / 1000.0),
         'board_on': post.board_on, 'created_by': post.created_by}
    replies = db_sess.query(Post).filter(Post.reply_to == post_id).order_by(Post.created_date.desc()).all()
    repl = []
    for i in replies:
        a = {'post': {'id': i.id, 'reply_to': i.reply_to, 'content': i.content,
                      'image': base64.b64encode(i.image).decode('utf-8') if i.image else None, 'file': i.file,
                      'created_date': datetime.datetime.fromtimestamp(i.created_date / 1000.0),
                      'board_on': i.board_on, 'created_by': i.created_by},
             'replies': []}
        for j in db_sess.query(Post).filter(Post.reply_to == i.id).order_by(Post.created_date.desc()).limit(3).all():
            a['replies'].append({'id': j.id, 'reply_to': j.reply_to, 'content': j.content,
                                 'image': base64.b64encode(j.image).decode('utf-8') if j.image else None,
                                 'file': j.file,
                                 'created_date': datetime.datetime.fromtimestamp(j.created_date / 1000.0),
                                 'board_on': j.board_on, 'created_by': j.created_by})
        repl.append(a)
    return render_template('post.html', title='Пост №' + str(post.id), d=d, repl=repl)


@app.route('/board/<board>/new', methods=['GET', 'POST'])
@login_required
def create_thread(board):
    form = ThreadForm()
    if form.validate_on_submit():
        thread = Post()
        thread.reply_to = -1

        thread.content = form.content.data
        thread.created_date = int(datetime.datetime.now().timestamp()) * 1000
        thread.board_on = board
        thread.created_by = current_user.name

        if form.image.data:
            f = form.image.data
            thread.image = f.read()

        if form.file.data:
            f = form.file.data
            filename = secure_filename(f.filename)
            thread.file = filename
            db_sess.add(thread)
            db_sess.commit()
            f.save(os.path.join('uploads', str(db_sess.query(Post).filter(Post.created_date == thread.created_date,
                                                                          Post.created_by == thread.created_by,
                                                                          Post.board_on == thread.board_on).first().id) + '.data'))
        else:
            db_sess.add(thread)
            db_sess.commit()

        return redirect(f'/board/{board}')
    return render_template('new_thread.html', title='Создание треда', form=form, board=board)


@app.route('/post/<int:post_id>/reply', methods=['GET', 'POST'])
@login_required
def create_reply(post_id):
    post = db_sess.query(Post).filter(Post.id == post_id).first()
    d = {'id': post.id, 'reply_to': post.reply_to, 'content': post.content,
         'image': base64.b64encode(post.image).decode('utf-8') if post.image else None, 'file': post.file,
         'created_date': datetime.datetime.fromtimestamp(post.created_date / 1000.0),
         'board_on': post.board_on, 'created_by': post.created_by}

    form = ReplyForm()
    if form.validate_on_submit():
        reply = Post()
        reply.reply_to = post_id

        reply.content = form.content.data
        reply.created_date = int(datetime.datetime.now().timestamp()) * 1000
        reply.board_on = d['board_on']
        reply.created_by = current_user.name

        if form.image.data:
            f = form.image.data
            reply.image = f.read()

        if form.file.data:
            f = form.file.data
            filename = secure_filename(f.filename)
            reply.file = filename
            db_sess.add(reply)
            db_sess.commit()
            f.save(os.path.join('uploads', str(db_sess.query(Post).filter(Post.created_date == reply.created_date,
                                                                          Post.created_by == reply.created_by,
                                                                          Post.board_on == reply.board_on).first().id) + '.data'))
        else:
            db_sess.add(reply)
            db_sess.commit()

        return redirect(f'/post/{post_id}')

    return render_template('reply.html', title='Ответ на №' + str(post.id), form=form, d=d)


@app.route('/user/<user>/update', methods=['GET', 'POST'])
@login_required
def update_user(user):
    usr = db_sess.query(User).filter(User.name == user).first()
    if current_user.name != usr.name:
        return redirect(f'/user/{user}')
    form = UserForm()
    if form.validate_on_submit():
        if form.description.data:
            usr.description = form.description.data
        else:
            usr.description = ''
        if form.image.data:
            f = form.image.data
            usr.picture = f.read()
        else:
            usr.picture = None
        db_sess.commit()
        return redirect(f'/user/{user}')

    return render_template('update_usr.html', title='Настройка профиля', user=user, form=form)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/register')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


db_session.global_init("db/base.db")
db_sess = db_session.create_session()
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=False)

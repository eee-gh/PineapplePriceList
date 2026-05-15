from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    name = StringField('Логин', validators=[DataRequired(), Length(3, 12)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(4, 16)])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
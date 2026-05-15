from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(3, 12)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(4, 16)])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), Length(4, 16)])
    submit = SubmitField('Зарегистрироваться')
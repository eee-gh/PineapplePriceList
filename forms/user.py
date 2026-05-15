from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, FileField, SubmitField


class UserForm(FlaskForm):
    description = TextAreaField('Описание', validators=[])
    image = FileField('Картинка', validators=[FileAllowed(['jpg', 'png', 'jpeg'],
                                                             'Выберите изображение')])
    submit = SubmitField('Подтвердить')
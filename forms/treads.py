from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, FileField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class TreadForm(FlaskForm):
    content = TextAreaField('Текст', validators=[DataRequired()])
    image = FileField('Изображение', validators=[FileAllowed(['jpg', 'png', 'jpeg'],
                                                             'Выберите изображение')])
    file = FileField('Файл')
    submit = SubmitField('Создать')

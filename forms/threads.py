from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired


class ThreadForm(FlaskForm):
    content = TextAreaField('Текст', validators=[DataRequired()])
    image = FileField('Изображение', validators=[FileAllowed(['jpg', 'png', 'jpeg'],
                                                             'Выберите изображение')])
    file = FileField('Файл')
    submit = SubmitField('Создать')

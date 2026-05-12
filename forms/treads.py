from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class TreadForm(FlaskForm):
    content = TextAreaField('Текст', validators=[DataRequired()])
    image = TextAreaField()
    file = TextAreaField()
    submit = SubmitField('Создать')

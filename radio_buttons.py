from flask_wtf import FlaskForm
from wtforms import SubmitField,RadioField
from wtforms.validators import InputRequired


class Quiz_Form(FlaskForm):
    question = RadioField(u'Question',
                          choices=[('1', 'Choice 1'), ('2', 'Choice 2'), ('3', 'Choice 3')],
                          validators=[InputRequired(message="Choose right answer")]
                          )
    submit = SubmitField("Submit")
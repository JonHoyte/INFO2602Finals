from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import InputRequired, EqualTo

class LogIn(FlaskForm):
  username = StringField('Username', validators=[InputRequired()])
  password = PasswordField('Password', validators=[InputRequired()])
  submit = SubmitField('Login', render_kw={'class': 'btn purple waves-effect waves-orange white-text'})

class Status(FlaskForm):
  Thought = TextAreaField(validators=[InputRequired()])
  submit = SubmitField('Add Post', render_kw={'class': 'btn purple waves-effect waves-light white-text'})
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=3)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=2, max=50)])
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=25)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    submit = SubmitField("Join now")


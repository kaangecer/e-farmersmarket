from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField
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

class CartForm(FlaskForm):
    full_name = StringField("Full name", validators=[InputRequired(), Length(min=2, max=50)])
    address = StringField("Address", validators=[InputRequired(), Length(min=5, max=200)])
    city = StringField("City", validators=[InputRequired(), Length(min=2, max=50)])
    zip_code = StringField("ZIP code", validators=[InputRequired(), Length(min=4, max=10)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    payment_method = SelectField(
        "Payment method",
        choices=[
            ("pickup_cash", "Pay on pickup (cash)"),
            ("digital_payment", "Digital payment"),
        ],
        validators=[InputRequired()],
    )
    submit = SubmitField("Place order")



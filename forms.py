from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length

class EmailOnlyLoginForm(FlaskForm):
    email = StringField(
        "E-Mail",
        validators=[InputRequired("Bitte E-Mail eingeben."), Email("Bitte gültige E-Mail eingeben.")]
    )
    submit = SubmitField("Weiter")

class PasswordOnlyLoginForm(FlaskForm):
    password = PasswordField(
        "Passwort",
        validators=[InputRequired("Bitte Passwort eingeben."), Length(min=6, message="Passwort muss mindestens 6 Zeichen lang sein.")]
    )
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[InputRequired("Bitte Name eingeben."), Length(min=2, max=50, message="Name muss zwischen 2 und 50 Zeichen lang sein.")]
    )
    username = StringField(
        "Benutzername",
        validators=[InputRequired("Bitte Benutzernamen eingeben."), Length(min=3, max=25, message="Benutzername muss zwischen 3 und 25 Zeichen lang sein.")]
    )
    password = PasswordField(
        "Passwort",
        validators=[InputRequired("Bitte Passwort eingeben."), Length(min=6, message="Passwort muss mindestens 6 Zeichen lang sein.")]
    )
    submit = SubmitField("Jetzt beitreten")

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



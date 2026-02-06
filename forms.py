from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, StringField, SelectField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Regexp, NumberRange

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
    first_name = StringField(
        "Vorname", validators=[InputRequired(), Length(min=2, max=50)]
        )
    last_name = StringField(
        "Nachname", validators=[InputRequired(), Length(min=2, max=50)]
        )
    username = StringField(
        "Benutzername",
        validators=[InputRequired("Bitte Benutzernamen eingeben."), Length(min=3, max=25, message="Benutzername muss zwischen 3 und 25 Zeichen lang sein.")]
    )
    password = PasswordField(
        "Passwort",
        validators=[InputRequired("Bitte Passwort eingeben."), Length(min=6, message="Passwort muss mindestens 6 Zeichen lang sein.")]
    )
    password_confirm = PasswordField(
        "Passwort bestätigen",
        validators=[InputRequired("Bitte Passwort bestätigen."), 
                    EqualTo("password", message="Passwörter stimmen nicht überein.")],
    )
    submit = SubmitField("Jetzt beitreten")

class SignupFormProducers(FlaskForm):
    # User table data
    username = StringField(
        "Benutzername",
        validators=[InputRequired("Bitte Benutzernamen eingeben."), Length(min=3, max=25, message="Benutzername muss zwischen 3 und 25 Zeichen lang sein.")],
    )
    first_name = StringField(
        "Geschäftsführer Vorname",
        validators=[InputRequired(), Length(min=2, max=50)],
    )
    last_name = StringField(
        "Geschäftsführer Nachname",
        validators=[InputRequired(), Length(min=2, max=50)],
    )
    email = StringField(
        "Login-E-Mail",
        validators=[InputRequired(), Email(), Length(max=255)],
    )
    password = PasswordField(
        "Passwort",
        validators=[
            InputRequired(),
            Length(min=6, message="Passwort muss mindestens 6 Zeichen haben."),
        ],
    )
    password_confirm = PasswordField(
        "Passwort bestätigen",
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwörter stimmen nicht überein."),
        ],
    )
    # Producers table data
    display_name = StringField(
        "Anzeigename (öffentlich)",
        validators=[InputRequired(), Length(min=2, max=255)],
    )
    legal_name = StringField(
        "Rechtlicher Name (optional)",
        validators=[Length(max=255)],
    )
    tax_id = StringField(
        "Steuer-/USt-ID (optional)",
        validators=[Length(max=50)],
    )
    contact_email = StringField(
        "Kontakt-E-Mail (für Kunden sichtbar)",
        validators=[InputRequired(), Email(), Length(max=255)],
    )
    contact_phone = StringField(
        "Telefon (optional)",
        validators=[Length(max=50)],
    )
    # Address data (for Address model)
    street = StringField(
        "Straße und Hausnummer",
        validators=[InputRequired(), Length(min=3, max=255)],
    )
    zip = StringField(
        "PLZ",
        validators=[
            InputRequired(),
            Length(min=4, max=10),
            Regexp(r"^[0-9]+$", message="Bitte nur Ziffern eingeben."),
        ],
    )
    city = StringField(
        "Stadt",
        validators=[InputRequired(), Length(min=2, max=100)],
    )
    country = StringField(
        "Land",
        validators=[InputRequired(), Length(min=2, max=100)],
    )
    submit = SubmitField("Als Produzent registrieren")

class ProductForm(FlaskForm):
    category_id = SelectField(
        "Kategorie",
        coerce=int,
        validators=[InputRequired("Bitte eine Kategorie auswählen.")],
    )
    name = StringField(
        "Produktname",
        validators=[InputRequired(), Length(min=2, max=255)],
    )
    description = TextAreaField(
        "Beschreibung",
        validators=[Length(max=2000)],
    )
    price = DecimalField(
        "Preis (€)",
        places=2,
        rounding=None,
        validators=[InputRequired(), NumberRange(min=0)],
    )
    is_active = BooleanField("Aktiv anzeigen")

    submit = SubmitField("Speichern")

class EditAddressForm(FlaskForm):
    street = StringField(
        "Straße und Hausnummer",
        validators=[InputRequired(), Length(min=3, max=255)],
    )
    zip = StringField(
        "PLZ",
        validators=[
            InputRequired(),
            Length(min=4, max=10),
        ],
    )
    city = StringField(
        "Stadt",
        validators=[InputRequired(), Length(min=2, max=100)],
    )
    country = StringField(
        "Land",
        validators=[InputRequired(), Length(min=2, max=100)],
    )

    submit = SubmitField("Adresse speichern")

class EditProducerProfileForm(FlaskForm):
    display_name = StringField(
        "Öffentlicher Name",
        validators=[InputRequired(), Length(min=2, max=255)],
    )
    legal_name = StringField(
        "Rechtlicher Name (optional)",
        validators=[Length(max=255)],
    )
    contact_email = StringField(
        "Kontakt-E-Mail",
        validators=[InputRequired(), Email(), Length(max=255)],
    )
    contact_phone = StringField(
        "Telefon (optional)",
        validators=[Length(max=50)],
    )

    submit = SubmitField("Profil speichern")

class CartForm(FlaskForm):
    first_name = StringField("First name", validators=[InputRequired(), Length(min=2, max=50)])
    last_name = StringField("Last name", validators=[InputRequired(), Length(min=2, max=50)])
    address = StringField("Address", validators=[InputRequired(), Length(min=5, max=200)])
    city = StringField("City", validators=[InputRequired(), Length(min=2, max=50)])
    zip_code = StringField("ZIP code", 
                           validators=[
                               InputRequired(),
                               Length(min=4, max=10),
                               Regexp(r"^[0-9]+$", message="Bitte nur Ziffern eingeben.")
                           ])
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



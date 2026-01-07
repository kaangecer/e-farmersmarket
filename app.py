from flask import Flask, render_template
from forms.forms import LoginForm, SignupForm, CartForm
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///farmersmarket.db"
app.config("SQLALCHEMY_TRACK_MODIFICATIONS") = False
db.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/producers")
def producers():
    return render_template("producers.html") 

#karte subpage
@app.route("/maps")
def maps():
    return render_template("maps.html") 

@app.route("/cart", methods=["GET", "POST"])
def cart():
    form = CartForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        address = form.address.data
        city = form.city.data
        zip_code = form.zip_code.data
        email = form.email.data
        payment_method = form.payment_method.data
        pass
    return render_template("cart.html", form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        pass
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        pass
    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)

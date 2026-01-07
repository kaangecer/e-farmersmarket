from flask import Flask, redirect, render_template, request, url_for
from forms import EmailOnlyLoginForm , PasswordOnlyLoginForm, SignupForm, CartForm
from models import User, db


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///farmersmarket.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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

@app.route("/login", methods=["GET", "POST"])
def login():
    step = request.args.get("step", "email")  # "email", "password", or "signup"
    email = request.args.get("email", "").strip().lower()

    if step == "email":
        form = EmailOnlyLoginForm()
        if form.validate_on_submit():
            email = form.email.data.strip().lower()
            user = User.query.filter_by(email=email).first()
            if user:
                return redirect(url_for("login", step="password", email=email))
            else:
                return redirect(url_for("login", step="signup", email=email))
        return render_template("login.html", step="email", email=email, form=form)
    
    if step == "password":
        form = PasswordOnlyLoginForm()
        if request.method == "GET" and email:
            # could show email read-only in template
            pass
        if form.validate_on_submit():
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            # TODO: check password properly (hash compare)
            if user and password == user.password:  # placeholder!
                return redirect(url_for("home"))
            else:
                form.password.errors.append("Falsches Passwort.")
        return render_template("login.html", step="password", email=email, form=form)
    
    if step == "signup":
        form = SignupForm()
        if request.method == "GET" and email and not form.name.data:
            # we keep email outside the form, but could add a hidden field if you want
            pass
        if form.validate_on_submit():
            name = form.name.data
            username = form.username.data
            password = form.password.data
            # TODO: create User row, hash password, commit
            user = User(email=email, password=password, role="CUSTOMER")
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("home"))
        return render_template("login.html", step="signup", email=email, form=form)
    else:  # treat anything else as signup
        form = SignupForm()
        return render_template("login.html", step="signup", email=email, form=form)

@app.route("/business")
def business():
    return render_template("business.html")

if __name__ == "__main__":
    app.run(debug=True)

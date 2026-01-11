from flask import Flask, redirect, render_template, request, url_for
from forms import EmailOnlyLoginForm , PasswordOnlyLoginForm, SignupForm, CartForm
from models import Category, Order, Product, User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = "login"

app.config["SECRET_KEY"] = "dev-secret-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///farmersmarket.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def products():
    products = Product.query.filter_by(is_active=True).all()
    categories = Category.query.all()
    return render_template("products.html", products=products, categories=categories)

@app.route("/producers")
def producers():
    producers = User.query.filter_by(role="PRODUCER").all()
    return render_template("producers.html", producers=producers)

@app.route("/maps")
def maps():
    return render_template("maps.html") 

@app.route("/cart", methods=["GET", "POST"])
def cart():
    form = CartForm()
    
    user_logged_in = current_user.is_authenticated

    if request.method == "GET" and user_logged_in:
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name

    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        address = form.address.data
        city = form.city.data
        zip_code = form.zip_code.data
        payment_method = form.payment_method.data
    return render_template("cart.html", form=form, user_logged_in=user_logged_in)

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
        if form.validate_on_submit():
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):  # placeholder!
                login_user(user)
                return redirect(url_for("home"))
            else:
                form.password.errors.append("Falsches Passwort.")
        return render_template("login.html", step="password", email=email, form=form)
    
    if step == "signup":
        form = SignupForm()
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            password = form.password.data

            user = User(
                email=email,
                password_hash=generate_password_hash(password),
                first_name=first_name,
                last_name=last_name,
                role="CUSTOMER"
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("home"))
        return render_template("login.html", step="signup", email=email, form=form)
    else:  # treat anything else as signup
        form = SignupForm()
        return render_template("login.html", step="signup", email=email, form=form)

@app.route("/account")
@login_required
def account():
    if current_user.customer_profile:
        customer_profile = current_user.customer_profile.orders.all()
    else:
        customer_profile = []
    return render_template("account.html", user=current_user, orders=customer_profile)

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/business")
def business():
    return render_template("business.html")

if __name__ == "__main__":
    app.run(debug=True)

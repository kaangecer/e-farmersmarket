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
    step = request.args.get("step", "email")
    email = request.args.get("email", "").strip().lower()

    if email:
        form = EmailOnlyLoginForm()
        if form.validate_on_submit():
            email = form.email.data.strip().lower()
            user = User.query.filter_by(email=email, role="PRODUCER").first()
            if user:
                return redirect(url_for("business", step="password", email=email))
            else:
                return redirect(url_for("business", step="signup", email=email))
        return render_template("business.html", step="email", email=email, form=form)
    
    if step == "password":
        form = PasswordOnlyLoginForm()
        if form.validate_on_submit():
            password = form.password.data
            user = User.query.filter_by(email=email, role="PRODUCER").first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for("business_account")) #wenn loged in, switch to business dashboard
            else:
                form.password.errors.append("Falsches Passwort.")
        return render_template("business.html", step="password", email=email, form=form)
    
    if step == "signup":
        form = SignupFormProducers()
        if form.validate_on_submit():
            user = User(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                email = form.email.data,
                role="PRODUCER"
            )
            user.set_password(form.password.data)
            db.session.add(user)

            address = Address(
                street=form.street.data,
                city=form.city.data,
                zip_code=form.zip_code.data,
                country=form.country.data
            )
            db.session.add(address)
            db.session.flush()

            producer_profile = ProducerProfile(
                user_id = user.id,
                address_id = address.address_id,
                display_name = form.display_name.data,
                legal_name = form.legal_name.data,
                tax_id = form.tax_id.data,
                contact_email = form.contact_email.data,
                contact_phone = form.contact_phone.data
            )
            db.session.add(producer_profile)

            db.session.commit()

            login_user(user)
            return redirect(url_for("business_account"))
        
        return render_template("business.html", step="signup", email=email, form=form)
    return redirect(url_for("business"))

@app.route("/business/account")
@login_required
def business_account():
    producer = current_user.producer_profile
    if not producer:
        return redirect(url_for("business"), step = "signup", email=current_user.email)
    products = producer.products.all()

    orders = []

    return render_template("business_account.html", producer=producer, products=products, orders=orders)

@app.route("/business/profile/edit", methods=["GET", "POST"])
@login_required
def edit_producer_profile():
    producer = current_user.producer_profile
    if not producer:
        return redirect(url_for("business_dashboard"))

    form = EditProducerProfileForm(obj=producer)
    if form.validate_on_submit():
        producer.display_name = form.display_name.data
        producer.legal_name = form.legal_name.data or None
        producer.contact_email = form.contact_email.data
        producer.contact_phone = form.contact_phone.data or None
        db.session.commit()
        return redirect(url_for("business_dashboard"))

    return render_template("edit_producer_profile.html", form=form)

@app.route("/address/edit", methods=["GET", "POST"])
@login_required
def edit_address():
    # Kundenadresse oder Producer-Adresse holen
    if current_user.role == "PRODUCER":
        producer = current_user.producer_profile
        address = producer.address
    else:
        # falls du eine direkte User-Address-Relation hast, sonst anpassen
        address = current_user.address  

    form = EditAddressForm(obj=address)

    if form.validate_on_submit():
        address.street = form.street.data
        address.zip = form.zip_code.data
        address.city = form.city.data
        address.country = form.country.data
        db.session.commit()

        # Nach Rollentyp zurückleiten
        if current_user.role == "PRODUCER":
            return redirect(url_for("business_dashboard"))
        else:
            return redirect(url_for("account"))

    return render_template("edit_address.html", form=form)

@app.route("/business/products/new", methods=["GET", "POST"])
@login_required
def create_product():
    producer = current_user.producer_profile
    if not producer:
        return redirect(url_for("business_dashboard"))

    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            is_active=True,
            producer_id=producer.producer_id,
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("business_dashboard"))

    return render_template("product_form.html", form=form)
    

@app.route("/business/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    producer = current_user.producer_profile
    product = Product.query.filter_by(
        id=product_id,
        producer_id=producer.producer_id
    ).first_or_404()

    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.is_active = form.is_active.data
        db.session.commit()
        return redirect(url_for("business_dashboard"))

    return render_template("product_form.html", form=form, product=product)

@app.route("/business/orders/<int:order_id>")
@login_required
def business_order_detail(order_id):
    producer = current_user.producer_profile
    # TODO: restrict to orders containing this producer's products
    order = Order.query.get_or_404(order_id)
    return render_template("business_order_detail.html", order=order)

if __name__ == "__main__":
    app.run(debug=True)

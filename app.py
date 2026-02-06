from decimal import Decimal
import profile
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from forms import EditAddressForm, EditProducerProfileForm, EmailOnlyLoginForm , PasswordOnlyLoginForm, ProductForm, SignupForm, CartForm, SignupFormProducers
from models import Address, Category, CustomerProfile, Order, OrderItem, ProducerProfile, Product, User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

# app setup with login manager, db connection, 

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = "login" # redirect unauthenticated users when accessing protected routes 

app.config["SECRET_KEY"] = "dev-secret-change-me" # for session management, cryptographic key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///farmersmarket.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # efficency feature
print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"]) # simple terminal debugging feature

db.init_app(app)

#user speichern und user_id laden
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# home page route
@app.route("/")
def home():
    map_pins = [
        {"label": "Hof Mayer", "x": 30, "y": 36, "color": "green"},
        {"label": "Kleins Garten", "x": 56, "y": 30, "color": "yellow"},
        {"label": "Bio Eierhof Schulz", "x": 52, "y": 62, "color": "red"},
        {"label": "Milchhof Bauer", "x": 68, "y": 48, "color": "green"},
        {"label": "Metzgerei Huber", "x": 40, "y": 54, "color": "yellow"},
    ]
    return render_template("home.html", map_pins=map_pins)

# produkte seite: aktive Produkte + Kategorien anzeigen
@app.route("/products")
def products():
    products = Product.query.filter_by(is_active=True).all()
    categories = Category.query.all()
    return render_template("products.html", products=products, categories=categories)

@app.route("/producer/<int:producer_id>/json")
def producer_json(producer_id):
    producer = ProducerProfile.query.get_or_404(producer_id)
    addr = producer.address
    return {
        "display_name": producer.display_name,
        "contact_email": producer.contact_email,
        "address": f"{addr.street}, {addr.zip} {addr.city}, {addr.country}" if addr else "",
    }


@app.route("/producer/<int:producer_id>")
def producer_detail(producer_id):
    producer = ProducerProfile.query.get_or_404(producer_id)
    return render_template("producer_details.html", producer=producer)


@app.post("/cart/add-json")
def add_to_cart_json():
    data = request.get_json(silent=True)
    app.logger.info("ADD_TO_CART_JSON payload: %r", data)

    product_id = str(data.get("product_id"))
    quantity = int(data.get("quantity", 1))

    if not product_id:
        return jsonify({"ok": False, "error": "Missing product_id"}), 400

    cart = get_cart()
    cart[product_id] = cart.get(product_id, 0) + quantity
    save_cart(cart)

    app.logger.info("Cart after add: %r", cart)

    total_items = sum(cart.values())
    return jsonify({"ok": True, "total_items": total_items})


# produzenten: ProducerProfile anzeigen von Producer table
@app.route("/producers")
def producers():
    producers = ProducerProfile.query.all()
    return render_template("producers.html", producers=producers, current_zip="", current_type="")

# Karte: Map-Seite anzeigen
@app.route("/maps")
def maps():
    return render_template("maps.html") 


@app.route("/cart", methods=["GET", "POST"])
def cart():
    form = CartForm()
    user_logged_in = current_user.is_authenticated

    # Prefill form for logged-in users
    if request.method == "GET" and user_logged_in:
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
       
        profile = current_user.customer_profile
        addr = profile.address if profile else None

        if addr:
            form.address.data = addr.street
            form.city.data = addr.city
            form.zip_code.data = addr.zip

            
    # Build cart items from session for display
    cart_data = get_cart()
    items = []
    total = Decimal("0.00")

    if cart_data:
        product_ids = [int(pid) for pid in cart_data.keys()]
        products = Product.query.filter(Product.product_id.in_(product_ids)).all()
        for p in products:
            qty = cart_data.get(str(p.product_id), 0)
            line_total = p.price * qty
            total += line_total
            items.append({"product": p, "qty": qty, "line_total": line_total})

    # Handle form submit (checkout)
    if form.validate_on_submit():
        # ensure we have a logged in customer
        if not current_user.is_authenticated or current_user.customer_profile is None:
            return redirect(url_for("login", step="email", email=form.email.data))

        customer = current_user.customer_profile

        # rebuild from session to be safe
        cart_data = get_cart()
        if not cart_data:
            return redirect(url_for("cart"))

        product_ids = [int(pid) for pid in cart_data.keys()]
        products = Product.query.filter(Product.product_id.in_(product_ids)).all()

        order_total = Decimal("0.00")
        new_order = Order(
            customer_id=customer.customer_id,
            total_amount=Decimal("0.00"),  # set after items
        )
        db.session.add(new_order)
        db.session.flush()  # ensures new_order.order_id is available

        for p in products:
            qty = cart_data.get(str(p.product_id), 0)
            if qty <= 0:
                continue

            line_total = p.price * qty
            order_total += line_total

            item = OrderItem(
                order_id=new_order.order_id,
                product_id=p.product_id,
                producer_id=p.producer_id,   # important for your model
                quantity=qty,
                unit_price=p.price,
                line_total=line_total,
            )
            db.session.add(item)

        new_order.total_amount = order_total
        db.session.commit()

        # clear cart after successful order
        save_cart({})

        return redirect(url_for("account"))

    return render_template(
        "cart.html",
        form=form,
        user_logged_in=user_logged_in,
        items=items,
        total=total,
    )

def get_cart():
    return session.get("cart", {})  # {"product_id": quantity}

def save_cart(cart):
    session["cart"] = cart
    session.modified = True



# email first workflow for login and signup
@app.route("/login", methods=["GET", "POST"])
def login():

    step = request.args.get("step", "email") #wert aus der URL holen, schritt definieren
    email = request.args.get("email", "").strip().lower() 

    if step == "email":
        form = EmailOnlyLoginForm()
        if form.validate_on_submit():
            email = form.email.data.strip().lower() #get email from form
            user = User.query.filter_by(email=email).first() #check if user email exists
            if user and user.role != "CUSTOMER":
                form.email.errors.append("Dieser Login ist nur für Kunden. Bitte verwenden Sie den Business-Login.")
                return redirect(url_for("login", step="password", email=email))
            else:
                return redirect(url_for("login", step="signup", email=email))
        return render_template("login.html", step="email", email=email, form=form)
    
    if step == "password":
        form = PasswordOnlyLoginForm()
        if form.validate_on_submit():
            password = form.password.data #get password from form
            user = User.query.filter_by(email=email).first() #find user by email, save in user variable
            if user and check_password_hash(user.password_hash, password):
                login_user(user) #log user in if password matches
                return redirect(url_for("home"))
            else:
                form.password.errors.append("Falsches Passwort.")
        return render_template("login.html", step="password", email=email, form=form)
    
    if step == "signup":
        form = SignupForm()
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = form.password.data
            username = form.username.data.strip()

            user = User(
                email=email,
                username=username,
                password_hash=generate_password_hash(password),
                first_name=first_name,
                last_name=last_name,
                role="CUSTOMER"
            )
            db.session.add(user)
            db.session.commit()

            customer_profile = CustomerProfile(user_id=user.id)
            db.session.add(customer_profile)
            db.session.commit()

            login_user(user) #remember loged in user
            return redirect(url_for("home"))
        return render_template("login.html", step="signup", email=email, form=form)
    
    else:  # treat anything else as signup
        form = SignupForm()
        return render_template("login.html", step="signup", email=email, form=form)

# account settings page
@app.route("/account")
@login_required
def account():
    user = current_user
    profile = user.customer_profile
    address = profile.address if profile else None
    form = EditAddressForm(obj=address)

    if profile:
        orders = profile.orders.options(db.joinedload(Order.items).joinedload(OrderItem.product)).all()
    else:
        orders = []

    return render_template("account.html", user=user, orders=orders, address=address, form=form)


# Logout
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# Business (Producer): Email first workflow for login and signup
@app.route("/business", methods=["GET", "POST"])
def business():
    step = request.args.get("step", "landing")
    email = request.args.get("email", "").strip().lower()

    if step == "landing":
        form = EmailOnlyLoginForm()
        if form.validate_on_submit():
            email = form.email.data.strip().lower()
            user = User.query.filter_by(email=email, role="PRODUCER").first()
            if user:
                return redirect(url_for("business", step="password", email=email))
            else:
                return redirect(url_for("business", step="signup", email=email))
        return render_template("business.html", step="landing", email=email, form=form)
    
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
        if email and not form.email.data:
            form.email.data = email
        if form.validate_on_submit():
            signup_email = (form.email.data or email).strip().lower()
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=signup_email,
                username=form.username.data.strip(),
                role="PRODUCER",
                password_hash=generate_password_hash(form.password.data),
            )

            db.session.add(user)
            db.session.flush()

            address = Address(
                street=form.street.data,
                zip=form.zip.data,
                city=form.city.data,
                country=form.country.data
            )
            db.session.add(address)
            db.session.flush()

            producer_profile = ProducerProfile(
                user_id=user.id,
                address_id=address.address_id,
                display_name=form.display_name.data,
                legal_name=form.legal_name.data,
                tax_id=form.tax_id.data,
                contact_email=form.contact_email.data,
                contact_phone=form.contact_phone.data
            )
            db.session.add(producer_profile)
            db.session.commit()

            login_user(user)
            return redirect(url_for("business_account"))
        
        return render_template("business.html", step="signup", email=email, form=form)
    # else:  # treat anything else as signup
    #     form = SignupForm()
    # return render_template("business.html", step="signup", email=email, form=form)


# business settings: Producer-Profil + Produkte anzeigen
@app.route("/business/account")
@login_required
def business_account():
    producer = current_user.producer_profile
    if not producer:
        return redirect(url_for("business"), step="signup", email=current_user.email) #verify that user is producer

    products = producer.products.all()
    orders = []
    return render_template("business_account.html", producer=producer, products=products, orders=orders)



# producer profil bearbeiten
@app.route("/business/profile/edit", methods=["GET", "POST"])
@login_required
def edit_producer_profile():
    producer = current_user.producer_profile #get current user's producer profile
    if not producer:
        return redirect(url_for("business_account"))

    form = EditProducerProfileForm(obj=producer) #populate form with object, existing data
    if form.validate_on_submit():
        producer.display_name = form.display_name.data
        producer.legal_name = form.legal_name.data or None
        producer.contact_email = form.contact_email.data
        producer.contact_phone = form.contact_phone.data or None
        db.session.commit()
        return redirect(url_for("business_account"))

    return render_template("edit_producer_profile.html", form=form)



# adresse bearbeiten (Customer oder Producer)
@app.route("/address/edit", methods=["GET", "POST"])
@login_required
def edit_address():
    if current_user.role == "PRODUCER":
        profile = current_user.producer_profile
        back_endpoint = "business"
    else:
        profile = current_user.customer_profile
        back_endpoint = "account"

    if profile is None:
        print("No profile found for user")
        return redirect(url_for(back_endpoint))
    
    address = profile.address

    # falls addresse nicht existiert, erstelle eine
    if address is None:
        address = Address(street="", zip="", city="", country="")
        db.session.add(address)
        db.session.flush()           # erzeugt address.address_id
        profile.address = address    # setzt profile.address_id
        db.session.commit()

    #wenn adresse besteht, aber geandert werden mochte
    form = EditAddressForm()

    if form.validate_on_submit():
        address.street = form.street.data
        address.zip = form.zip.data
        address.city = form.city.data
        address.country = form.country.data
        db.session.commit()
        print("SAVED ADDRESS:", address.street, address.zip, address.city, address.country)
    
        return redirect(url_for(back_endpoint))

    return render_template(f"{back_endpoint}.html", form=form, address=address)



# Produkt anlegen (Producer)
@app.route("/business/products/new", methods=["GET", "POST"])
@login_required
def create_product():
    producer = current_user.producer_profile
    if not producer:
        return redirect(url_for("business_account"))

    form = ProductForm()
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
        return redirect(url_for("business_account"))

    return render_template("product_form.html", form=form)
    


# Produkt bearbeiten (Producer)
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
        return redirect(url_for("business_account"))

    return render_template("product_form.html", form=form, product=product)



# Order-Detail (Producer)
@app.route("/business/orders/<int:order_id>")
@login_required
def business_order_detail(order_id):
    producer = current_user.producer_profile
    order = Order.query.get_or_404(order_id)
    return render_template("business_order_detail.html", producer=producer, order=order)



# Account löschen (Customer oder Producer)
@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    user = User.query.get(current_user.id)
    
    db.session.delete(user)
    db.session.commit()
    
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

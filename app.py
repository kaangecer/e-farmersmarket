from flask import Flask, render_template
from forms.forms import LoginForm, SignupForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-change-me"

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

#warenkorb subpage
@app.route("/cart")
def cart():
    return render_template("cart.html")

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

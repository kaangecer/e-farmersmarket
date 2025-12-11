from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def products():
    return render_template("products.html")  # TODO: create

@app.route("/producers")
def producers():
    return render_template("producers.html")  # TODO: create

#karte subpage
@app.route("/maps")
def maps():
    return render_template("maps.html")  # TODO: create

#warenkorb subpage
@app.route("/cart")
def cart():
    return render_template("cart.html")  # TODO: create

@app.route("/signup", methods=["GET", "POST"])
def signup():
    # later you can handle form POST here
    return render_template("signup.html") # UI screen

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")  # UI screen

if __name__ == "__main__":
    app.run(debug=True)

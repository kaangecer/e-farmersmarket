from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")  # UI screen

@app.route("/products")
def products():
    return render_template("products.html")  # TODO: create

@app.route("/producers")
def producers():
    return render_template("producers.html")  # TODO: create

@app.route("/join", methods=["GET", "POST"])
def join():
    # later you can handle form POST here
    return render_template("join.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")  # UI screen

if __name__ == "__main__":
    app.run(debug=True)

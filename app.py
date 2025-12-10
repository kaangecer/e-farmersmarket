from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")  # UI screen

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")  # UI screen

if __name__ == "__main__":
    app.run(debug=True)

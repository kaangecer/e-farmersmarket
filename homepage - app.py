from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

PRODUCTS = [
    {
        "id": 1,
        "name": "Bio Äpfel",
        "category": "Obst",
        "price": 3.50,
        "zip": "10115",
        "bio": True,
        "producer_id": 1
    },
    {
        "id": 2,
        "name": "Kartoffeln festkochend",
        "category": "Gemüse",
        "price": 2.20,
        "zip": "10439",
        "bio": False,
        "producer_id": 2
    },
    {
        "id": 3,
        "name": "Freilandeier (10 Stück)",
        "category": "Eier",
        "price": 4.00,
        "zip": "12045",
        "bio": True,
        "producer_id": 1
    },
]

PRODUCERS = [
    {
        "id": 1,
        "name": "Hof Sonnenfeld",
        "type": "Bauernhof",
        "zip": "10115",
        "description": "Familienbetrieb mit Fokus auf Bio-Gemüse und Obst."
    },
    {
        "id": 2,
        "name": "Kiez Hofladen Kreuzberg",
        "type": "Hofladen",
        "zip": "10997",
        "description": "Regionale Produkte von Höfen im Umland."
    },
    {
        "id": 3,
        "name": "Omas Garten",
        "type": "Hobbygärtner",
        "zip": "12045",
        "description": "Überschüssiges Obst und Gemüse aus Privatanbau."
    },
]


@app.route("/")
def home():
    demo_product = PRODUCTS[0] if PRODUCTS else None
    demo_producer = PRODUCERS[0] if PRODUCERS else None
    return render_template(
        "index.html",
        demo_product=demo_product,
        demo_producer=demo_producer
    )


@app.route("/products")
def products():
    query = request.args.get("q", "").strip().lower()
    zip_filter = request.args.get("zip", "").strip()
    category = request.args.get("category", "").strip()
    bio_only = request.args.get("bio") == "on"

    filtered = PRODUCTS

    if query:
        filtered = [p for p in filtered if query in p["name"].lower()]

    if zip_filter:
        filtered = [p for p in filtered if p["zip"].startswith(zip_filter)]

    if category:
        filtered = [p for p in filtered if p["category"] == category]

    if bio_only:
        filtered = [p for p in filtered if p["bio"]]

    return render_template(
        "products.html",
        products=filtered,
        current_query=query,
        current_zip=zip_filter,
        current_category=category,
        current_bio=bio_only
    )


@app.route("/producers")
def producers():
    zip_filter = request.args.get("zip", "").strip()
    producer_type = request.args.get("type", "").strip()

    filtered = PRODUCERS

    if zip_filter:
        filtered = [p for p in filtered if p["zip"].startswith(zip_filter)]

    if producer_type:
        filtered = [p for p in filtered if p["type"] == producer_type]

    return render_template(
        "producers.html",
        producers=filtered,
        current_zip=zip_filter,
        current_type=producer_type
    )


@app.route("/auth", methods=["GET", "POST"])
def auth():
    mode = request.args.get("mode", "login")

    if request.method == "POST":
        return redirect(url_for("home"))

    return render_template("auth.html", mode=mode)


if __name__ == "__main__":
    app.run(debug=True)

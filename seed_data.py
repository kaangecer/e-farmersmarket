# seed_data.py
from werkzeug.security import generate_password_hash
from app import app, db
from models import (
    User, Address, ProducerProfile, Product, Category,
    CustomerProfile, Cart, CartItem, Order, OrderItem,
)


def seed_producers_and_products():
    print("Clearing existing data...")

    OrderItem.query.delete()
    Order.query.delete()
    CartItem.query.delete()
    Cart.query.delete()
    Product.query.delete()
    ProducerProfile.query.delete()
    CustomerProfile.query.delete()
    Address.query.delete()
    Category.query.delete()
    User.query.delete()
    db.session.commit()

    # Categories
    category_names = ["Obst", "Gemüse", "Eier", "Milchprodukte", "Fleisch"]
    categories = {}
    for name in category_names:
        cat = Category(name=name)
        db.session.add(cat)
        db.session.flush()
        categories[name] = cat

    producer_defs = [
        {
            "display_name": "Hof Mayer",
            "username": "hof_mayer",
            "email": "hof.mayer@example.com",
            "password": "Test12345!",
            "first_name": "Anna",
            "last_name": "Mayer",
            "street": "Feldweg 12",
            "zip_code": "80331",
            "city": "München",
            "country": "Deutschland",
            "contact_email": "kontakt@hofmayer.de",
            "phone": "+49 170 1111111",
            "category": "Obst",
            "products": [
                {
                    "name": "Elstar Äpfel, 1kg",
                    "description": "Frische Elstar Äpfel direkt vom Hof, ideal als Tafelapfel.",
                    "price": 2.99,
                },
                {
                    "name": "Conference Birnen, 1kg",
                    "description": "Saftige Birnen aus regionalem Anbau.",
                    "price": 3.49,
                },
                {
                    "name": "Zwetschgen, 500g",
                    "description": "Süße Zwetschgen, perfekt für Kuchen oder zum Naschen.",
                    "price": 2.79,
                },
            ],
        },
        {
            "display_name": "Kleins Garten",
            "username": "kleins_garten",
            "email": "garten.klein@example.com",
            "password": "Test12345!",
            "first_name": "Lukas",
            "last_name": "Klein",
            "street": "Gartenstraße 5",
            "zip_code": "50667",
            "city": "Köln",
            "country": "Deutschland",
            "contact_email": "info@kleinsgarten.de",
            "phone": "+49 170 2222222",
            "category": "Gemüse",
            "products": [
                {
                    "name": "Karotten, 1kg",
                    "description": "Knackige Bundkarotten aus Freilandanbau.",
                    "price": 2.29,
                },
                {
                    "name": "Speisekartoffeln festkochend, 2kg",
                    "description": "Festkochende Kartoffeln, ideal für Bratkartoffeln und Salat.",
                    "price": 3.99,
                },
                {
                    "name": "Romana Salatherzen, 2 Stück",
                    "description": "Frische Romana-Salatherzen für knackige Salate.",
                    "price": 2.49,
                },
            ],
        },
        {
            "display_name": "Bio Eierhof Schulz",
            "username": "eierhof_schulz",
            "email": "eierhof.schulz@example.com",
            "password": "Test12345!",
            "first_name": "Maria",
            "last_name": "Schulz",
            "street": "Hühnerweg 3",
            "zip_code": "10115",
            "city": "Berlin",
            "country": "Deutschland",
            "contact_email": "kontakt@eierhof-schulz.de",
            "phone": "+49 170 3333333",
            "category": "Eier",
            "products": [
                {
                    "name": "Bio-Eier Bodenhaltung, 10 Stück",
                    "description": "Frische Bio-Eier aus Bodenhaltung vom Hof Schulz.",
                    "price": 3.99,
                },
                {
                    "name": "Bio-Eier Freiland, 6 Stück",
                    "description": "Freilandeier mit extra viel Auslauf für die Hühner.",
                    "price": 3.49,
                },
                {
                    "name": "Bunte Eier, 10 Stück",
                    "description": "Hart gekochte und gefärbte Eier, ideal für Frühstück und Buffet.",
                    "price": 4.29,
                },
            ],
        },
        {
            "display_name": "Milchhof Bauer",
            "username": "milchhof_bauer",
            "email": "milchhof.bauer@example.com",
            "password": "Test12345!",
            "first_name": "Johann",
            "last_name": "Bauer",
            "street": "Kuhweg 9",
            "zip_code": "20095",
            "city": "Hamburg",
            "country": "Deutschland",
            "contact_email": "info@milchhof-bauer.de",
            "phone": "+49 170 4444444",
            "category": "Milchprodukte",
            "products": [
                {
                    "name": "Frische Vollmilch, 1L",
                    "description": "Pasteurisierte Vollmilch mit 3,8% Fett aus regionaler Haltung.",
                    "price": 1.49,
                },
                {
                    "name": "Naturjoghurt im Glas, 500g",
                    "description": "Cremiger Naturjoghurt ohne Zuckerzusatz.",
                    "price": 1.99,
                },
                {
                    "name": "Schnittkäse mild, 200g",
                    "description": "Milder Hofkäse, ideal für Brotzeit und Toast.",
                    "price": 3.29,
                },
            ],
        },
        {
            "display_name": "Metzgerei Huber",
            "username": "metzgerei_huber",
            "email": "metzgerei.huber@example.com",
            "password": "Test12345!",
            "first_name": "Franz",
            "last_name": "Huber",
            "street": "Marktstraße 7",
            "zip_code": "80331",
            "city": "München",
            "country": "Deutschland",
            "contact_email": "kontakt@metzgerei-huber.de",
            "phone": "+49 170 5555555",
            "category": "Fleisch",
            "products": [
                {
                    "name": "Rinderhackfleisch, 500g",
                    "description": "Frisches Rinderhack aus regionaler Haltung.",
                    "price": 5.49,
                },
                {
                    "name": "Schweineschnitzel, 2 Stück",
                    "description": "Zarte Schweineschnitzel, fertig zum Panieren.",
                    "price": 4.99,
                },
                {
                    "name": "Bratwurst grob, 4 Stück",
                    "description": "Hausgemachte grobe Bratwürste für Pfanne oder Grill.",
                    "price": 4.59,
                },
            ],
        },
    ]

    for pdef in producer_defs:
        user = User(
            username=pdef["username"],
            email=pdef["email"].lower(),
            password_hash=generate_password_hash(pdef["password"]),
            first_name=pdef["first_name"],
            last_name=pdef["last_name"],
            role="PRODUCER",
        )
        db.session.add(user)
        db.session.flush()

        address = Address(
            street=pdef["street"],
            zip=pdef["zip_code"],
            city=pdef["city"],
            country=pdef["country"],
        )
        db.session.add(address)
        db.session.flush()

        producer = ProducerProfile(
            user_id=user.id,
            address_id=address.address_id,
            display_name=pdef["display_name"],
            contact_email=pdef["contact_email"].lower(),
            contact_phone=pdef["phone"],
        )
        db.session.add(producer)
        db.session.flush()

        cat = categories[pdef["category"]]
        for prod_def in pdef["products"]:
            product = Product(
                name=prod_def["name"],
                description=prod_def["description"],
                price=prod_def["price"],
                producer_id=producer.producer_id,
                category_id=cat.category_id,
                is_active=True,
            )
            db.session.add(product)

        print(f"OK: Producer angelegt: {pdef['display_name']} ({pdef['email']})")

    db.session.commit()
    print("Fertig: Alle Daten gelöscht, 5 Produzenten + echte Produkte neu angelegt.")


if __name__ == "__main__":
    with app.app_context():
        seed_producers_and_products()

from app import app, db
from models import ProducerProfile, Category, Product, User, Address
from datetime import datetime
from decimal import Decimal

with app.app_context():
    # 1) Create a dummy user and address for the producer
    producer_user = User(
        email="producer@example.com",
        password_hash="dummy",  # or a real hash if you want
        first_name="Local",
        last_name="Farmer",
        role="PRODUCER",
    )
    db.session.add(producer_user)
    db.session.flush()  # get producer_user.id

    producer_address = Address(
        street="Hauptstraße 1",
        city="Berlin",
        zip="10115",
        country="Deutschland",
    )
    db.session.add(producer_address)
    db.session.flush()  # get address_id

    producer = ProducerProfile(
        user_id=producer_user.id,
        address_id=producer_address.address_id,
        display_name="Biohof Sonnental",
        legal_name="Biohof Sonnental GmbH",
        tax_id="DE123456789",
        contact_email="kontakt@biohof-sonnental.de",
        contact_phone="+49 30 1234567",
        verification_status="verified",
    )
    db.session.add(producer)

    # 2) Create categories
    category_names = [
        "Produce",          # Gemüse etc.
        "Milk products",    # Milch, Käse, Joghurt
        "Eggs",
        "Fruit",
        "Meats",
    ]
    categories = []
    for name in category_names:
        cat = Category(name=name)
        db.session.add(cat)
        categories.append(cat)

    db.session.flush()  # get category_ids

    # Helper: pick categories by name
    cat_by_name = {c.name: c for c in categories}

    # 3) Create 20 products
    products = [
        # Produce
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Produce"].category_id,
            name="Carrots",
            description="Crunchy organic carrots from the farm.",
            price=Decimal("1.80"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Produce"].category_id,
            name="Zucchini",
            description="Fresh zucchini, ideal for grilling.",
            price=Decimal("2.10"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Produce"].category_id,
            name="Cherry Tomatoes",
            description="Sweet cherry tomatoes for salads and snacks.",
            price=Decimal("2.90"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Produce"].category_id,
            name="Baby Spinach",
            description="Tender baby spinach leaves.",
            price=Decimal("2.40"),
        ),

        # Milk products
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Milk products"].category_id,
            name="Whole Milk 1L",
            description="Fresh whole milk from grass-fed cows.",
            price=Decimal("1.40"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Milk products"].category_id,
            name="Natural Yogurt",
            description="Plain yogurt with live cultures.",
            price=Decimal("1.20"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Milk products"].category_id,
            name="Goat Cheese",
            description="Soft goat cheese with mild flavor.",
            price=Decimal("5.90"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Milk products"].category_id,
            name="Butter",
            description="Creamy farm butter, ideal for baking.",
            price=Decimal("2.30"),
        ),

        # Eggs
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Eggs"].category_id,
            name="Free-range Eggs (10 pcs)",
            description="Eggs from free-range hens.",
            price=Decimal("3.50"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Eggs"].category_id,
            name="Organic Eggs (6 pcs)",
            description="Certified organic eggs.",
            price=Decimal("3.10"),
        ),

        # Fruit
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Fruit"].category_id,
            name="Apples",
            description="Mixed varieties of fresh apples.",
            price=Decimal("3.20"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Fruit"].category_id,
            name="Pears",
            description="Sweet, ripe pears.",
            price=Decimal("3.40"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Fruit"].category_id,
            name="Strawberries",
            description="Fresh strawberries (250g punnet).",
            price=Decimal("3.90"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Fruit"].category_id,
            name="Blueberries",
            description="Blueberries rich in antioxidants.",
            price=Decimal("4.20"),
        ),

        # Meats
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Meats"].category_id,
            name="Beef Mince",
            description="Minced beef from pasture-raised cattle.",
            price=Decimal("7.50"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Meats"].category_id,
            name="Pork Sausages",
            description="Farm-style pork sausages.",
            price=Decimal("5.20"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Meats"].category_id,
            name="Chicken Breast",
            description="Skinless chicken breast fillets.",
            price=Decimal("6.80"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Meats"].category_id,
            name="Smoked Ham",
            description="Traditional smoked ham.",
            price=Decimal("4.90"),
        ),
        Product(
            producer_id=producer.producer_id,
            category_id=cat_by_name["Meats"].category_id,
            name="Bone Broth",
            description="Slow-cooked beef bone broth.",
            price=Decimal("3.70"),
        ),
    ]

    db.session.add_all(products)
    db.session.commit()
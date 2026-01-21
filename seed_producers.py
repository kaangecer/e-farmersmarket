from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Address, ProducerProfile

def add_producer(email, password, first_name, last_name, display_name, street, zip_code, city, country, contact_email, phone=None):
    # schon vorhanden?
    existing = User.query.filter_by(email=email.lower()).first()
    if existing:
        print(f"SKIP: User existiert bereits: {email}")
        return

    user = User(
        email=email.lower(),
        password_hash=generate_password_hash(password),
        first_name=first_name,
        last_name=last_name,
        role="PRODUCER"
    )
    db.session.add(user)
    db.session.flush()  # user.id

    address = Address(
        street=street,
        zip=zip_code,      # WICHTIG: Feld heißt "zip" in deinem Model
        city=city,
        country=country
    )
    db.session.add(address)
    db.session.flush()  # address.address_id

    producer = ProducerProfile(
        user_id=user.id,
        address_id=address.address_id,
        display_name=display_name,
        contact_email=contact_email.lower(),
        contact_phone=phone
    )
    db.session.add(producer)

    db.session.commit()
    print(f"OK: Producer angelegt: {display_name} ({email})")

with app.app_context():
    add_producer(
        email="hof.mayer@example.com",
        password="Test12345!",
        first_name="Anna",
        last_name="Mayer",
        display_name="Hof Mayer",
        street="Feldweg 12",
        zip_code="80331",
        city="München",
        country="Deutschland",
        contact_email="kontakt@hofmayer.de",
        phone="+49 170 1111111"
    )

    add_producer(
        email="garten.klein@example.com",
        password="Test12345!",
        first_name="Lukas",
        last_name="Klein",
        display_name="Kleins Garten",
        street="Gartenstraße 5",
        zip_code="50667",
        city="Köln",
        country="Deutschland",
        contact_email="info@kleinsgarten.de",
        phone="+49 170 2222222"
    )

    print("Fertig.")

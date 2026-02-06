# reset_schema.py
from app import app, db
from models import *  # ensure models are imported so tables are registered

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables from current models...")
    db.create_all()
    db.session.commit()
    print("Done.")

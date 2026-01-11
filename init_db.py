from app import app, db
from models import ProducerProfile, Category, Product, User, Address
from datetime import datetime
from decimal import Decimal

with app.app_context():
    db.session.commit()
from app import app, db
from datetime import datetime
from decimal import Decimal
from models import (
    User, Address, CustomerProfile, ProducerProfile, Category, Product, Cart, Order, OrderItem, CartItem)

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    db.session.commit()
    print("Done")
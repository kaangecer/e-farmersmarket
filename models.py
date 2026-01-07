# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)        # CUSTOMER | PRODUCER
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    customer_profile = db.relationship("CustomerProfile", back_populates="user", uselist=False)
    producer_profile = db.relationship("ProducerProfile", back_populates="user", uselist=False)

class Address(db.Model):
    __tablename__ = "address"
    address_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class CustomerProfile(db.Model):
    __tablename__ = "customer_profile"
    customer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    default_address_id = db.Column(db.Integer, db.ForeignKey("address.address_id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="customer_profile")
    default_address = db.relationship("Address", backref="customers")

class ProducerProfile(db.Model):
    __tablename__ = "producer_profile"
    producer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False, unique=True)
    legal_name = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    tax_id = db.Column(db.String(50))
    address_id = db.Column(db.Integer, db.ForeignKey("address.address_id"))
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(50))
    verification_status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="producer_profile")
    address = db.relationship("Address", backref="producers")

class Category(db.Model):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.Integer, primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey("producer_profile.producer_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    producer = db.relationship("ProducerProfile", backref="products")
    category = db.relationship("Category", backref="products")

class PickupLocation(db.Model):
    __tablename__ = "pickup_location"
    pickup_location_id = db.Column(db.Integer, primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey("producer_profile.producer_id"), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("address.address_id"), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(100))
    opening_hours = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    producer = db.relationship("ProducerProfile", backref="pickup_locations")
    address = db.relationship("Address", backref="pickup_locations")

class Cart(db.Model):
    __tablename__ = "cart"
    cart_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer_profile.customer_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    customer = db.relationship("CustomerProfile", backref="carts")

class CartItem(db.Model):
    __tablename__ = "cart_item"
    cart_item_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.cart_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    producer_id = db.Column(db.Integer, db.ForeignKey("producer_profile.producer_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    cart = db.relationship("Cart", backref="items")
    product = db.relationship("Product")
    producer = db.relationship("ProducerProfile")

class Order(db.Model):
    __tablename__ = "order"
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer_profile.customer_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    pickup_type = db.Column(db.String(20), nullable=False)
    pickup_location_id = db.Column(db.Integer, db.ForeignKey("pickup_location.pickup_location_id"))

    customer = db.relationship("CustomerProfile", backref="orders")
    pickup_location = db.relationship("PickupLocation", backref="orders")

class OrderItem(db.Model):
    __tablename__ = "order_item"
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.order_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    producer_id = db.Column(db.Integer, db.ForeignKey("producer_profile.producer_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    line_total = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship("Order", backref="items")
    product = db.relationship("Product")
    producer = db.relationship("ProducerProfile")

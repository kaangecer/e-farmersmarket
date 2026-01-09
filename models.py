# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'CUSTOMER' | 'PRODUCER'
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

    customers = db.relationship("CustomerProfile", back_populates="address", lazy="dynamic")
    producers = db.relationship("ProducerProfile", back_populates="address", lazy="dynamic")


class CustomerProfile(db.Model):
    __tablename__ = "customer_profile"

    customer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("address.address_id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="customer_profile")
    address = db.relationship("Address", back_populates="customers")


class ProducerProfile(db.Model):
    __tablename__ = "producer_profile"

    producer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("address.address_id"), nullable=True)
    display_name = db.Column(db.String(255), nullable=False)
    legal_name = db.Column(db.String(255), nullable=True)
    tax_id = db.Column(db.String(50), nullable=True)
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(50), nullable=True)
    verification_status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="producer_profile")
    products = db.relationship("Product", back_populates="producer", lazy="dynamic")
    address = db.relationship("Address", back_populates="producers")


class Category(db.Model):
    __tablename__ = "category"

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    products = db.relationship("Product", back_populates="category", lazy="dynamic")

class Product(db.Model):
    __tablename__ = "product"

    product_id = db.Column(db.Integer, primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey("producer_profile.producer_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    producer = db.relationship("ProducerProfile", back_populates="products")
    category = db.relationship("Category", back_populates="products")

    cart_items = db.relationship("CartItem", back_populates="product", lazy="dynamic")
    order_items = db.relationship("OrderItem", back_populates="product", lazy="dynamic")


class Cart(db.Model):
    __tablename__ = "cart"

    cart_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer_profile.customer_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    customer = db.relationship("CustomerProfile", backref=db.backref("carts", lazy="dynamic"))
    items = db.relationship("CartItem", back_populates="cart", cascade="all, delete-orphan", lazy="dynamic")


class CartItem(db.Model):
    __tablename__ = "cart_item"

    cart_item_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.cart_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    producer_id = db.Column(db.Integer, db.ForeignKey("producer_profile.producer_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    cart = db.relationship("Cart", back_populates="items")
    product = db.relationship("Product", back_populates="cart_items")
    producer = db.relationship("ProducerProfile")

class Order(db.Model):
    __tablename__ = "order"

    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer_profile.customer_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)

    customer = db.relationship("CustomerProfile", backref=db.backref("orders", lazy="dynamic"))
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="dynamic")


class OrderItem(db.Model):
    __tablename__ = "order_item"

    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.order_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    producer_id = db.Column(db.Integer, db.ForeignKey("producer_profile.producer_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    line_total = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")
    producer = db.relationship("ProducerProfile")
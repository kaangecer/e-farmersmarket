# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
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
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("address.address_id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="customer_profile")
    address = db.relationship("Address", back_populates="customers")


class ProducerProfile(db.Model):
    __tablename__ = "producer_profile"

    producer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("address.address_id"), nullable=True)
    display_name = db.Column(db.String(255), nullable=False)
    legal_name = db.Column(db.String(255), nullable=True)
    tax_id = db.Column(db.String(50), nullable=True)
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(50), nullable=True)
    verification_status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="producer_profile")
    address = db.relationship("Address", back_populates="producers")

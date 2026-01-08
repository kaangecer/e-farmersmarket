from app import app
from models import db
import models  # ensure models are imported

with app.app_context():
    db.create_all()

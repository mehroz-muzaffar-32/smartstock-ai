from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to InventoryUpload
    uploads = db.relationship('InventoryUpload', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

class InventoryUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to InventoryItem
    items = db.relationship('InventoryItem', backref='upload', lazy=True)

    def __repr__(self):
        return f'<InventoryUpload {self.filename} by {self.user.email}>'

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(db.Integer, db.ForeignKey('inventory_upload.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<InventoryItem {self.name}: {self.quantity}>'

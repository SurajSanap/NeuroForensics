from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime 
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Criminal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    crime_details = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    face_encoding = db.Column(db.Text, nullable=False)  # New Column
    enable_yolo = db.Column(db.Boolean, default=True)  # Toggle YOLO
    yolo_model_path = db.Column(db.String(255), default="yolov8n.pt")  # Default YOLO model

class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    camera_name = db.Column(db.String(100), nullable=False)
    camera_url = db.Column(db.String(255), nullable=False)

    enable_face_detection = db.Column(db.Boolean, default=False)
    enable_weapon_detection = db.Column(db.Boolean, default=False)

class WeaponDetection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    weapon_type = db.Column(db.String(50))  # Gun, Knife, etc.
    confidence = db.Column(db.Float)  # Detection confidence
    image_path = db.Column(db.String(255))  # Screenshot of detection

# Database Models for PrioritySound 
# Defines the data structures stored in the SQLite database using SQLAlchemy ORM 

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User account model with authentication and preferences"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    preferences = db.Column(db.Text, nullable=True)  # JSON string of sound priorities
    mode = db.Column(db.String(50), nullable=True)   # Selected mode (Parent, Home, etc.)

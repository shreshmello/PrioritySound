from flask_sqlalchemy import SQLAlchemy

# Database object
db = SQLAlchemy()

# User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    email = db.Column(db.String(120), unique=True, nullable=False)  # User email
    password = db.Column(db.String(200), nullable=False)  # Hashed password
    preferences = db.Column(db.Text, nullable=True)  # JSON string of user preferences
    mode = db.Column(db.String(50), nullable=True)  # Current mode (e.g., "Parent", "Home")
